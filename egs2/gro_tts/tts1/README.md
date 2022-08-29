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

You can manually follow the GroTTS recipe and then put your files in the correct directory (See ```data/``` in [GroTTS](https://github.com/samin9796/gro-tts/tree/main/egs2/gro_tts/tts1/data)). Here, KALDI style data preparation is maintained.

#### 2. Wav dump / Embedding preparation

This stage can be skipped for Gronings data.

#### 3. Removal of long / short data

You can set the threshold values via ```--min_wav_duration``` and ```--max_wav_duration```. For Gronings dataset, this stage can be skipped.

#### 4. Token list generation

Token list generation stage. It generates token list (dictionary) from srctexts. Tokens are generated since during training the Tacotrons, it takes the character/phone units as input. You can change the tokenization type via ```--token_type``` option. ```token_type=char``` (characters) and ```token_type=phn``` (phones) are supported. If ```--cleaner``` option is specified, the input text will be cleaned with the specified cleaner (e.g. Using Tacotron cleaner: ```"(Hello-World); & jr. & dr."``` -> ```HELLO WORLD, AND JUNIOR AND DOCTOR```). If ```token_type=phn```, the input text will be converted with G2P module specified by ```--g2p``` option.

For Gronings, ```token_type=char``` has been used and the following command has been executed.

```
./run.sh --stage 4 --stop-stage 4 --token_type=char
```

Alternatively, you can manually set the ```--token_type``` in the config file.

#### 5. TTS statistics collection

It collects the shape information of the input and output and calculates statistics for feature normalization (mean and variance over training data). You can run the following command.

```
./run.sh --stage 5 --stop-stage 5
```

#### 6. TTS training

After stage 5 completes, you can run the following command. By default, Tacotron 2 architecture will be trained.

```
./run.sh --stage 6 --stop-stage 6
```

#### 7. TTS decoding

In this stage, you need to execute the following command.

```
./run.sh --stage 7 --stop-stage 7
```

### Training FastSpeech2

The stages 1-4 is exactly similar to Tacotron 2 training. If you have already run those stages, you do not need to go through again. You need to train Tacotron2 or Transformer-TTS at first which will be the teacher model to get the durations. If you have an existing Tacotron 2, you can just use that ([Link to pretrained Tacotron 2 on Gronings](https://huggingface.co/ahnafsamin/Tacotron2-gronings)). After that, you need to decode all of data in the following way.

``` 
    $ ./run.sh --stage 7 \
    --tts_exp exp/tts_train_raw_char_tacotron_g2p_en_no_space \
    --inference_args "--use_teacher_forcing true" \
    --test_sets "tr_no_dev dev eval1" 
```

Then, you need to perform stage 5 to calculate additional statistics (F0 and energy).

``` 
    $ ./run.sh --stage 5 \
    --train_config conf/tuning/train_fastspeech2.yaml \
    --teacher_dumpdir exp/tts_train_raw_char_tacotron_g2p_en_no_space/decode_use_teacher_forcingtrue_train.loss.ave \
    --tts_stats_dir exp/tts_train_raw_char_tacotron_g2p_en_no_space/decode_use_teacher_forcingtrue_train.loss.ave/stats \
    --write_collected_feats true
```
    
Finally, you can train FastSpeech 2 with the following command.

``` 
    $ ./run.sh --stage 6 \
    --train_config conf/tuning/train_fastspeech2.yaml \
    --teacher_dumpdir exp/tts_train_raw_char_tacotron_g2p_en_no_space/decode_use_teacher_forcingtrue_train.loss.ave 
```

Stage 7 (Decoding) is same as Tacotron2 decoding.

To train the neural vocoders, this [repo](https://github.com/kan-bayashi/ParallelWaveGAN) has been followed. Detailed documentation will be available soon in this repo.
