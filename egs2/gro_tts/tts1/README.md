## Gro-TTS Recipe

You need to follow the [ESPnet TTS Recipe template](https://github.com/espnet/espnet/tree/master/egs2/TEMPLATE/tts1) to get detailed information about training a model. In short, you can run the following commands for training models with your custom data:

#### Step 1: Clone the ESPnet repository
```
$ git clone https://github.com/espnet/espnet.git
```
#### Step 2: Download or follow the ```egs2/gro_tts/tts1``` recipe from this repository. Go to the recipe directory
```
$ cd egs2/gro_tts/tts1
```
#### Step 3: Training the model

There are 7 stages in TTS recipe. 

#### 1. Data preparation

You can manually follow the GroTTS recipe and then put your files in the correct directory (See ```data/``` in [GroTTS](https://github.com/samin9796/gro-tts/tree/main/egs2/gro_tts/tts1/data)). Here, KALDI style data preparation is maintained. The following five directories are prepared (you can ignore the ```train``` and ```deveval``` directories since these are not mandatory):

- ```train``` (contains both training and dev data)
- ```tr_no_dev``` (contains only training data)
- ```deveval``` (contains both dev and eval data)
- ```dev``` (contains only dev data)
- ```eval1``` (contains only eval data)

The ```data``` directory should look like the following:
```
data/
  train/
    - text     # The transcription
    - wav.scp  # Wave file path
    - utt2spk  # A file mapping utterance-id to speaker-id
    - spk2utt  # A file mapping speaker-id to utterance-id
  tr_no_dev/
    ...
  deveval/
    ...
  dev/
    ...
  eval1/
    ...
```

Each of the directores within the ```data``` directory needs to contain the four files in the following formats:

- ```text``` format

```
uttidA <transcription>
uttidB <transcription>
...
```
- ```wav.scp``` format

```
uttidA /path/to/uttidA.wav
uttidB /path/to/uttidB.wav
...
```
- ```utt2spk``` format

```
uttidA speakerA
uttidB speakerB
uttidC speakerA
uttidD speakerB
...
```

- ```spk2utt``` format

```
speakerA uttidA uttidC ...
speakerB uttidB uttidD ...
...
```

#### 2. Wav dump / Embedding preparation

You can manually prepare the ```/dump``` directory in the GroTTS recipe. It has the following structure:

```
├── dump/ # feature dump directory
│   ├── token_list/    # token list (dictionary)
│   └── raw/
│       ├── org/
│       │    ├── tr_no_dev/ # training set before filtering
│       │    └── dev/       # validation set before filtering
│       ├── srctexts   # text to create token list
│       ├── eval1/     # evaluation set
│       ├── dev/       # validation set after filtering
│       └── tr_no_dev/ # training set after filtering
```
Copy the ```tr_no_dev```, ```dev``` and ```eval``` directories from ```data``` folder and paste them according to the folder structure shown above. You can ignore the ```token_list``` directory for now which will be generated in stage 4. The ```srctexts``` file is the same as ```/tr_no_dev/text``` (just change the name of the file). For convenience, the ```/dump``` folder used for GroTTS recipe is provided [here](https://github.com/samin9796/gro-tts/tree/main/egs2/gro_tts/tts1/dump).

#### 3. Removal of long / short data

You can set the threshold values via ```--min_wav_duration``` and ```--max_wav_duration```. For Gronings dataset, this stage can be skipped since all the samples in this dataset have the proper audio length suitable for training.

#### 4. Token list generation

Token list generation stage. It generates token list (dictionary) from srctexts. An example of token list is provided below:

```
<blank>
<unk>
<space>
E
N
A
O
T
I
R
...
```
This token list can be found in [this directory](https://github.com/samin9796/gro-tts/blob/main/egs2/gro_tts/tts1/dump/token_list/char_tacotron/tokens.txt). The ```srctexts``` is the same file as ```tr_no_dev/text``` in ```data``` folder. The ```srctexts``` file is provided [here](https://github.com/samin9796/gro-tts/blob/main/egs2/gro_tts/tts1/dump/raw/srctexts). Notice that, this file should be put in the ```/dump/raw/``` directory.

Tokens are generated since during training the Tacotron 2 model, it takes the character/phone units as input. You can change the tokenization type via ```--token_type``` option. ```token_type=char``` (characters) and ```token_type=phn``` (phones) are supported. If ```--cleaner``` option is specified, the input text will be cleaned with the specified cleaner (e.g. Using Tacotron cleaner: ```"(Hello-World); & jr. & dr."``` -> ```HELLO WORLD, AND JUNIOR AND DOCTOR```). If ```token_type=phn```, the input text will be converted with G2P module specified by ```--g2p``` option.

For Gronings, ```token_type=char``` has been used and the following command has been executed.

```
./run.sh --stage 4 --stop-stage 4 --token_type char
```
To use ```token_type=phn``` for Gronings, a G2P converter for Gronings is required which is currently not available. Thus, ```token_type=char``` is used here.

Instead of passing the ```token_type``` as an argument in the command, you can also manually set the ```--token_type``` in the [config](https://github.com/samin9796/gro-tts/blob/main/egs2/gro_tts/tts1/exp/config.yaml) file.

#### 5. TTS statistics collection

It collects the [shape information](https://github.com/samin9796/gro-tts/tree/main/egs2/gro_tts/tts1/exp/tts_stats_raw_char_tacotron) of the input text and the output audio and calculates statistics for feature normalization (mean and variance over training data). The feature normalization is automatically applied in this step. You can run the following command.

```
./run.sh --stage 5 --stop-stage 5
```

#### 6. TTS training

After stage 5 completes, you can run the following command. By default, Tacotron 2 architecture will be trained. The parameters are specified in the [train.yaml](https://github.com/samin9796/gro-tts/blob/main/egs2/gro_tts/tts1/conf/train.yaml) file which can be found in the ```\conf``` folder. If you want to change the parameters, you can do that from ```train.yaml```. For Gronings, the default parameters set for the LJSpeech recipe are used. The only changes that have been made are ```batch_bins: 2000000``` and 
```accum_grad: 2``` to solve our limited GPU memory issue.
```
./run.sh --stage 6 --stop-stage 6
```

#### 7. TTS decoding

In this stage, you need to execute the following command. This command generates the audio files from the ```dev``` and ```eval``` sets and the synthesized audio files can be found in ```/exp``` directory. Thus, this stage is required to get the synthesized audio files which can be used as evaluating the model.

```
./run.sh --stage 7 --stop-stage 7
```

After completing the 7 stages, you will get the following directories in the recipe directory.

```
├── data/ # Kaldi-style data directory
│   ├── dev/        # validation set
│   ├── eval1/      # evaluation set
│   └── tr_no_dev/  # training set
├── dump/ # feature dump directory
│   ├── token_list/    # token list (dictionary)
│   └── raw/
│       ├── org/
│       │    ├── tr_no_dev/ # training set before filtering
│       │    └── dev/       # validation set before filtering
│       ├── srctexts   # text to create token list
│       ├── eval1/     # evaluation set
│       ├── dev/       # validation set after filtering
│       └── tr_no_dev/ # training set after filtering
└── exp/ # experiment directory
    ├── tts_stats_raw_char_tacotron_g2p_en_no_space # statistics
    └── tts_train_raw_char_tacotron_g2p_en_no_space # model
        ├── att_ws/                # attention plot during training
        ├── tensorboard/           # tensorboard log
        ├── images/                # plot of training curves
        ├── decode_train.loss.ave/ # decoded results
        │    ├── dev/   # validation set
        │    └── eval1/ # evaluation set
        │        ├── att_ws/      # attention plot in decoding
        │        ├── probs/       # stop probability plot in decoding
        │        ├── norm/        # generated features
        │        ├── denorm/      # generated denormalized features
        │        ├── wav/         # generated wav via Griffin-Lim
        │        ├── log/         # log directory
        │        ├── durations    # duration of each input tokens
        │        ├── feats_type   # feature type
        │        ├── focus_rates  # focus rate
        │        └── speech_shape # shape info of generated features
        ├── config.yaml             # config used for the training
        ├── train.log               # training log
        ├── *epoch.pth              # model parameter file
        ├── checkpoint.pth          # model + optimizer + scheduler parameter file
        ├── latest.pth              # symlink to latest model parameter
        ├── *.ave_5best.pth         # model averaged parameters
        └── *.best.pth              # symlink to the best model parameter loss
        
```
### Training FastSpeech2

The above-mentioned stages are for training the Tacotron 2 model. For training FastSpeech 2, the stages 1-4 is exactly similar to Tacotron 2 training. If you have already run those stages, you do not need to go through the steps again. You need to train Tacotron2 or Transformer-TTS at first which will be the teacher model to get the phone durations. Phone durations are extracted from the attention weights of a pre-trained Tacotron 2 system (See [FastSpeech 2](https://arxiv.org/abs/2006.04558) paper for details). The duration file from the Tacotron 2 has the following format:

```
identifier1 first_phone_duration second_phone_duration ...
identifier2 first_phone_duration second_phone_duration ...
...
```

Example:
```
a-1 9 16 9 3 5 4 5 6 8 6 8 2 8 5 12 5 6 7 4 16 0 24 12 19 4 3 5 5 5 10 13 3 4 10 4 8 9 0 10 13 8 3 5 4 1 5 4 6 6 6 6 3 7 2 4 3 2 2 2 5 3 4 9 5 17 23 20 11 1 7 3 8 5 5 6 5 0 7 4 5 1 4 4 4 6 4 10 8 1 10 26 10 7 2 6 4 6 6 6 7 9 11 8 1 3 6 3 8 14 3 10 20
a-10 17 10 12 2 9 14 7 12 14 6 11 19 33 19 8 5 6 8 6 2 17 4 7 3 7 3 5 1 8 6 8 3 5 5 7 3 14 28 25 7 4 5 5 4 6 8 7 5 2 12 4 10 9 6 7 3 6 5 7 4 3 7 21 45
a-100 0 9 3 4 5 4 6 7 2 3 3 6 5 5 3 9 0 15 5 3 3 2 3 4 6 4 5 6 3 5 9 23 2 6 4 4 3 6 5 6 9 6 1 7 3 6 6 2 10 5 8 1 4 3 3 7 5 4 3 5 4 8 0 11 12 1 4 4 5 5 4 8 6 1 7 2 6 0 6 3 4 0 5 0 5 2 7 2 7 4 5 5 5 4 6 12 12
a-1000 8 11 4 4 3 7 3 6 6 6 4 1 3 4 8 5 3 4 5 4 4 11 3 15 11 10 3 3 7 4 5 4 5 2 1 2 4 3 3 2 0 6 2 5 2 9 6 12 3 25 1 7 7 5 8 5 1 7 4 4 2 4 4 6 7 5 6 6 11 6
a-1001 7 7 3 4 5 4 5 6 1 8 4 2 3 4 2 4 1 3 2 3 4 8 4 4 5 4 5 3 4 4 4 4 5 3 6 8 5 15
```


If you have an existing Tacotron 2, you can just use that ([Link to pretrained Tacotron 2 on Gronings](https://huggingface.co/ahnafsamin/Tacotron2-gronings)). Download the Tacotron 2 and paste it to the ```/exp/tts_train_raw_char_tacotron_g2p_en_no_space``` directory. After that, you need to decode all of data in the following way.

``` 
    $ ./run.sh --stage 7 \
    --tts_exp exp/tts_train_raw_char_tacotron_g2p_en_no_space \
    --inference_args "--use_teacher_forcing true" \
    --test_sets "tr_no_dev dev eval1" 
```

Then, you need to perform stage 5 to calculate additional statistics (F0 and energy). By running the following command, the training will also start.

``` 
    $ ./run.sh --stage 5 \
    --train_config conf/tuning/train_fastspeech2.yaml \
    --teacher_dumpdir exp/tts_train_raw_char_tacotron_g2p_en_no_space/decode_use_teacher_forcingtrue_train.loss.ave \
    --tts_stats_dir exp/tts_train_raw_char_tacotron_g2p_en_no_space/decode_use_teacher_forcingtrue_train.loss.ave/stats \
    --write_collected_feats true
```


Here, the parameter ```train_config``` refers to the configuration file for training the fastspeech2 model. You can change the architecture, learning rate, batch bins etc. from the ```conf/tuning/train_fastspeech2.yaml``` file. Another parameter ```teacher_dumpdir``` refers to the directory where all the phone durations are located. The ```exp/tts_train_raw_char_tacotron_g2p_en_no_space/decode_use_teacher_forcingtrue_train.loss.ave``` directory will automatically be generated since you have already run the stage 7 above.

If you face ```RuntimeError: Keys are mismatched.``` error, visit the following [link](https://github.com/espnet/espnet/issues/4336) for solution.

### Training Vocoders

Please follow this [link](https://github.com/kan-bayashi/ParallelWaveGAN) to train a vocoder using your custom dataset.
