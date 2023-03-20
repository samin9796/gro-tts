# Speech Synthesis for Gronings

In this project, we implement several state-of-the-art Text-to-Speech (TTS) architectures for Gronings, a Low Saxon language spoken in the province of Groningen and around the Groningen border in Drenthe and Friesland in the Netherlands.[^1]

To build TTS systems for Gronings, [ESPnet2](https://github.com/espnet/espnet), a speech processing toolkit has been utilized. The setup configuration and installation steps that have been followed based on the original [documentation](https://espnet.github.io/espnet/installation.html) to develop the TTS systems are documented below.

## Install ESPnet2 locally

### Setup Configuration

For the experiments, the following setup has been used. It is not necessary to have this exact configuration, however, compatibility between different versions must be ensured.
- Ubuntu 20.04 LTS
- Python 3.8.12
- CUDA version 11.1 (run ```nvcc -V``` to check it)
- CUDA Driver version 470.103.01 (run ```nvidia-smi``` to check it)
- CUDA version 11.4 (run ```nvidia-smi``` to check it)
- PyTorch 1.10.1+cu111

### Step 1: Install the following packages

- cmake
- sox
- sndfile
- ffmpeg
- flac

The following command will install all the above packages.
```
 $ sudo apt-get install cmake sox libsndfile1-dev ffmpeg flac
```

### Step 2: Installation
1. Git clone the ESPnet repo
```
$ cd <any-place>
$ git clone https://github.com/espnet/espnet
```
2. Setup Anaconda Environment

You have to create ``` <espnet-root>/tools/activate_python.sh.``` to specify the Python interpreter used in ESPnet recipes. To do so:
```
$ cd <espnet-root>/tools
$ ./setup_anaconda.sh [output-dir-name|default=venv] [conda-env-name|default=root] [python-version|default=none]
# e.g.
$ ./setup_anaconda.sh anaconda espnet 3.8
```
3. Install ESPnet

The Makefile tries to install ESPnet and all dependencies including PyTorch. You can specify the PyTorch version (must be compatible with your CUDA version), for example:
```
$ cd <espnet-root>/tools
$ make TH_VERSION=1.10.1+cu111
```
Note that the CUDA version is derived from the ```nvcc``` command. Alternatively, you can also specify the CUDA version.
```
$ cd <espnet-root>/tools
$ make TH_VERSION=1.10.1+cu111 CUDA_VERSION=11.1
```

### Step 3: Check Installation

Note that all the packages are not required to be installed for TTS development.
```
$ cd <espnet-root>/tools
$ . ./activate_python.sh; python3 check_install.py
```

## Text-to-Speech Systems

The following architectures and neural vocoders have been implemented for Gronings:
- Architecture
  - [FastSpeech 2](https://arxiv.org/abs/2006.04558)
  - [Conformer FastSpeech 2](https://arxiv.org/pdf/2010.13956.pdf)
  - [Tacotron 2](https://arxiv.org/abs/1712.05884)
- Neural Vocoder
  - [Parallel Wavegan](https://arxiv.org/abs/1910.11480)
  - [Hifi-gan](https://arxiv.org/abs/2010.05646)
  
FastSpeech 2 has been implemented in two ways.
1. Using Tacotron 2 as the Teacher Forced Aligner
2. Using [Montreal Forced Aligner](https://mfa-models.readthedocs.io/en/latest/acoustic/Dutch/Dutch%20CV%20acoustic%20model%20v2_0_0.html#Dutch%20CV%20acoustic%20model%20v2_0_0) to get the alignments

The procedure of training the architectures and vocoders can be found in [recipe](https://github.com/samin9796/gro-tts/tree/main/egs2/gro_tts/tts1) and [neural vocoder](https://github.com/kan-bayashi/ParallelWaveGAN).

## Results, Online Demo and Pre-trained Models

<details>
  <summary>Results</summary>
  
  You can listen to the generated samples from [here](https://drive.google.com/drive/folders/1djf6HOUUieKIgmvKyJThBh3V_5MfjEqJ?usp=sharing).
  
  | Dataset  | Architecture | Vocoder | Mean Opinion Score (MOS) |
  | ------------- | ------------- | ------------- | ------------- |
  | Gronings  | Ground Truth  | -  | -  |
  | Gronings  | Tacotron 2  | Parallel Wavegan  | -  |
  | Gronings  | FastSpeech 2  | Parallel Wavegan  | -  |
  | Gronings  | Conformer FastSpeech 2  | Parallel Wavegan  | -  |
  | Gronings  | Tacotron 2  | Hifi-gan  | -  |
  | Gronings  | FastSpeech 2  | Hifi-gan  | -  |
  | Gronings  | Conformer FastSpeech 2  | Hifi-gan  | -  |

</details>

<details>
  <summary>Online Demo</summary>
  
  The real-time demo is available on [HuggingFace](https://huggingface.co/spaces/ahnafsamin/GroTTS-FastSpeech2)! 
  
  FastSpeech 2 (using Tacotron 2 as Teacher Forced Aligner) and a pre-trained Parallel Wavegan vocoder have been used here. This vocoder is pre-trained on English data since the current ESPnet+HuggingFace integration does not allow to use vocoder trained on custom data.
</details>

<details>
  <summary>Pre-trained Models</summary>
  
  The following models are trained on approx. 2 hours of Gronings speech data and can be available on HuggingFace!
  
  - [Fast Speech 2](https://huggingface.co/ahnafsamin/FastSpeech2-gronings) (using Tacotron 2 as Teacher Forced Aligner)
  - [Tacotron 2](https://huggingface.co/ahnafsamin/Tacotron2-gronings)
  - [Parallel Wavegan vocoder](https://huggingface.co/ahnafsamin/parallelwavegan-gronings)
  
</details>

## References
[^1]: https://en.wikipedia.org/wiki/Gronings_dialect.
