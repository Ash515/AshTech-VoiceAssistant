# Voxpopuli- Lokesh(Maintainer)
[![PyPI](https://img.shields.io/pypi/v/voxpopuli.svg)](https://pypi.python.org/pypi/voxpopuli)
[![PyPI](https://img.shields.io/pypi/pyversions/voxpopuli.svg)](http://py3readiness.org/)
[![Build Status](https://travis-ci.org/hadware/voxpopuli.svg?branch=master)](https://travis-ci.org/hadware/voxpopuli)
[![Documentation Status](https://readthedocs.org/projects/voxpopuli/badge/?version=latest)](http://voxpopuli.readthedocs.io/en/latest/?badge=latest)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](LICENSE)


**A wrapper around Espeak and Mbrola.**

This is a lightweight Python wrapper for Espeak and Mbrola, two co-dependent TTS tools. It enables you to 
render sound by simply feeding it text and voice parameters. Phonems (the data transmitted by Espeak to
mbrola) can also be manipulated using a mimalistic API.

This is a short introduction, but you might want to look at the [readthedoc documentation](http://voxpopuli.readthedocs.io/en/latest/).

## Install

### Linux (Ubuntu)
Install with pip as:
```sh
pip install voxpopuli
```

You have to have espeak and mbrola installed beforehand:
```sh
sudo apt install mbrola espeak
```

You'll also need some mbrola voices installed, which you can either get on their project page, 
and then uppack in `/usr/share/mbrola/<lang><voiceid>/` or more simply by 
installing them from the ubuntu repo's. All the voices' packages are of the form
`mbrola-<lang><voiceid>`. You can even more simply install all the voices available
by running:
```sh
sudo apt install mbrola-*
```

In case the voices you need aren't all in the ubuntu repo's, you can use this convenient little script
that install voices diretcly from [Mbrola's voice repo](https://github.com/numediart/MBROLA-voices):
```sh
# this installs all british english and french voices for instance
sudo python3 -m voxpopuli.voice_install en fr
```

### Windows installation

**Note: this might be out oudated, since Mbrola's website has been replaced by github repositories. If you're willing to try and use voxpopuli 
on windows and succeeded at setting it up, please do submit a pull request to update this documentation.**

* `pip install voxpopuli`
* Download and install espeak: http://sourceforge.net/projects/espeak/files/espeak/espeak-1.48/setup_espeak-1.48.04.exe
* Download and install mbrola: https://tcts.fpms.ac.be/synthesis/mbrola/bin/pcwin/MbrolaTools35.exe
* Download mbrola DOS binary: http://tcts.fpms.ac.be/synthesis/mbrola/bin/pcdos/mbr301d.zip
* Unpack the .zip archive and put `mbrola.exe` into your mbrola folder.
* Download voice files you need: https://tcts.fpms.ac.be/synthesis/mbrola/mbrcopybin.html
* Unpack them into a single location (the default is `%USERPROFILE%\.mbrola`) so that each voice package is in its own folder
* From each voice folder copy the main file (for example `fr1`) and put it in `\espeak-data\mbrola` folder in your epeak installation.

**Important!**

If your mbrola voices folder is not in the default location, don't forget to set its location after importing `Voice` module:

```python
from voxpopuli import Voice
Voice.mbrola_voices_folder = 'D:\\mbrola-voices\\'
```

Repeat the above with `Voice.espeak_binary` and `Voice.mbrola_binary` if you installed them in non-default locations.

## Usage

### Picking a voice and making it say things

The most simple usage of this lib is just bare TTS, using a voice and
a text. The rendered audio is returned in a .wav bytes object:
```python
from voxpopuli import Voice
voice = Voice(lang="fr")
wav = voice.to_audio("salut c'est cool")
```
Evaluating `type(wav)` whould return `bytes`. You can then save the wav using the `wb` 
file option

```python
with open("salut.wav", "wb") as wavfile:
    wavfile.write(wav)
```
If you wish to hear how it sounds right away, you'll have to make sure you installed pyaudio *via* pip, and then do:
```python
voice.say("Salut c'est cool")
```

Ou can also, say, use scipy to get the pcm audio as a `ndarray`:

```python
import scipy.io.wavfile import read, write
from io import BytesIO

rate, wave_array = read(BytesIO(wav))
reversed = wave_array[::-1] # reversing the sound file
write("tulas.wav", rate, reversed)
```

### Getting different voices

You can set some parameters you can set on the voice, such as language or pitch

```python
from voxpopuli import Voice
# really slow fice with high pitch
voice = Voice(lang="us", pitch=99, speed=40, voice_id=2)
voice.say("I'm high on helium")
```

The exhaustive list of parameters is:

 * lang, a language code among those available (us, fr, en, es, ...) You can list
    them using the `listvoices` method from a `Voice` instance.
 * voice_id, an integer, used to select the voice id for a language. If not specified,
    the first voice id found for a given language is used.
 * pitch, an integer between 0 and 99 (included)
 * speed, an integer, in the words per minute. Default and regular speed
is 160 wpm.
 * volume, float ratio applied to the output sample. Some languages have presets
    that our best specialists tested. Otherwise, defaults to 1.

### Handling the phonemic form

To render a string of text to audio, the Voice object actually chains espeak's output
to mbrola, who then renders it to audio. Espeak only renders the text to a list of
phonemes (such as the one in the IPA), who then are to be processed by mbrola.
For those who like pictures, here is a diagram of what happens when you run
`voice.to_audio("Hello world")`

![phonemes](docs/source/img/phonemes.png?raw=true)

phonemes are represented sequentially by a code, a duration in milliseconds, and
a list of pitch modifiers. The pitch modifiers are a list of couples, each couple
representing the percentage of the sample at which to apply the pitch modification and
the pitch. 

Funny thing is, with voxpopuli, you can "intercept" that phoneme list as a
simple object, modify it, and then pass it back to the voice to render it to
audio. For instance, let's make a simple alteration that'll double the
duration for each vowels in an english text.

```python
from voxpopuli import Voice, BritishEnglishPhonemes

voice = Voice(lang="en")
# here's how you get the phonemes list
phoneme_list = voice.to_phonemes("Now go away or I will taunt you a second time.") 
for phoneme in phoneme_list: #phoneme list object inherits from the list object
    if phoneme.name in BritishEnglishPhonemes.VOWELS:
        phoneme.duration *= 3
        
# rendering and saving the sound, then saying it out loud:
voice.to_audio(phoneme_list, "modified.wav")
voice.say(phoneme_list)
```

Notes:

 * For French, Spanish, German and Italian, the phoneme codes
 used by espeak and mbrola are available as class attributes similar to the `BritishEnglishPhonemes` class as above.
 * More info on the phonemes can be found here: [SAMPA page](http://www.phon.ucl.ac.uk/home/sampa/)


## What's left to do

 * A real sphinx documentation

 * Moar unit tests

 * Maybe some examples

   
