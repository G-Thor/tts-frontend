
# TTS Textprocessing Pipeline for Icelandic

This project provides a TTS textprocessing pipeline for Icelandic. The pipeline includes modules for html parsing, text cleaning, text normalization for TTS, spell and grammar correction, phrasing, and grapheme-to-phoneme (g2p) conversion. Before a text can be fed into a TTS system it has to be converted into the format that was used when training that system. The format can be grapheme-based (i.e. alphabetic characters of the language in question are used as input) or phoneme-based (i.e. a phonetic alphabet like IPA or SAMPA are used as input). The TTS Textprocessing Pipeline for Icelandic offers both possibilities.

## The Pipeline

The TTS frontend pipeline makes seamless text preprocessing for TTS using different submodules possible. It manages tags, e.g. SSML tags, that might be added or processed at different stages, and stores the processing history of each token from original input, through normalizing and correction to phonetic representation at the end of the pipeline.

## Prerequisites and setup

You can install the project either by cloning the repository and install from the project root, or you can install
directly from github. Assuming you have Python > 3.6 installed:

```
$ # clone and install:
$ git clone https://github.com/grammatek/tts-frontend.git
$ cd tts-frontend
$ # create a virtual env
$ python3 -m venv <path/to/your/venv>
$ source <path/to/your/venv>/bin/activate
(venv) $ pip install -e .
```

If you run into ``wheel`` error, install ``wheel`` before you install this project:

```
$ (venv) pip install wheel
$ (venv) pip install -e .
```
Install for use in an existing project

```
$ # make sure you are in your project folder with the virtual environment activated
(venv) $ pip install git+https://github.com/grammatek/tts-frontend
```

**NOTE:** The setup works with `pip 21.3.1` , upgrading pip to a newer version caused fairseq
installation to fail (see unresolved issue here: https://github.com/pytorch/fairseq/issues/3535)

## Usage

The text processing pipeline can be run from input text to transcribed output, or partly run, e.g. only
normalizing the input. The text_processor returns a list of tokens, including all information collected on 
each token, including token index and character spans from original text. Examples (for further options, study 
[textprocessing_manager.py](https://github.com/grammatek/tts-frontend/blob/master/src/manager/textprocessing_manager.py)): 

```
from manager.textprocessing_manager import Manager

text_processor = Manager()
input_text = 'Sunnan 4 m/s'
normalized_as_token_list = text_processor.normalize(input_text)
normalized_as_string = text_processor.get_string_representation_normalized(normalized_as_token_list) 
```

Output:

```
input_text: 'Sunnan 4 m/s'
normalized_as_token_list:

Normalized: [
Token:
Original: Sunnan, Clean: Sunnan,
Tokenized: ['Sunnan'],
Normalized: [Sunnan, nhen]
Transcribed: []
index: 0, 0, 6
, 
Token:
Original: 4, Clean: 4,
Tokenized: ['4'],
Normalized: [fjórir, ta]
Transcribed: []
index: 1, 7, 8
, 
Token:
Original: m/s, Clean: m/s,
Tokenized: ['m/s'],
Normalized: [metrar, nkfn, á, af, sekúndu, nveþ]
Transcribed: []
index: 2, 9, 12
, TagToken(<sentence>, 3)]

normalized_as_string: 'Sunnan fjórir metrar á sekúndu'

```

Full pipeline with g2p:

```
from manager.textprocessing_manager import Manager

text_processor = Manager()
input_text = 'Sunnan 4 m/s'
transcribed_as_token_list = text_processor.transcribe(input_text)
transcribed_as_string = text_processor.get_string_representation_transcribed(transcribed_as_token_list)
```

Output:

```
input_text: 'Sunnan 4 m/s'
transcribed_as_token_list:

Transcribed: [
Token:
Original: Sunnan, Clean: Sunnan,
Tokenized: ['Sunnan'],
Normalized: [Sunnan, nhen]
Transcribed: ['s Y n a n']
index: 0, 0, 6
, 
Token:
Original: 4, Clean: 4,
Tokenized: ['4'],
Normalized: [fjórir, ta]
Transcribed: ['f j ou: r I r']
index: 1, 7, 8
, 
Token:
Original: m/s, Clean: m/s,
Tokenized: ['m/s'],
Normalized: [metrar, nkfn, á, af, sekúndu, nveþ]
Transcribed: ['m E: t r a r', 'au:', 's E: k u n t Y']
index: 2, 9, 12
, TagToken(<sentence>, 3)]

transcribed_as_string: s Y n a n f j ou: r I r m E: t r a r au: s E: k u n t Y
```


## Credits
This is a fork of Grammatek ehf.'s tts-frontend, but has undergone significant refactoring by Gunnar Thor Örnólfsson at [Reykjavik University's 
LVL](https://lvl.ru.is/).

The adapted code from the [phrasing tool](https://github.com/grammatek/phrasing-tool/tree/tts-frontend) and [normalizer](https://github.com/grammatek/regina_normalizer/tree/tts-frontend) has been integrated into this package, removing all reliance on submodules.

Those tools were originally forked from the [Reykjavik University
LVL](https://lvl.ru.is/) Github repository, and adapted by Grammatek.

The IceNLP package as well as the ABL-tagger used in the project were developed at RU LVL.

## License and copyright

![Grammatek](grammatek-logo-small.png)](https://www.grammatek.com)

Copyright © 2022 Grammatek ehf.

This software is developed under the auspices of the Icelandic Government 5-Year Language Technology Program, described
[here](https://www.stjornarradid.is/lisalib/getfile.aspx?itemid=56f6368e-54f0-11e7-941a-005056bc530c) and
[here](https://clarin.is/media/uploads/mlt-en.pdf) (English).

This software is licensed under the [Apache License](LICENSE)

## Contributing / Contact
You can contribute to this project by forking it, creating a private branch and opening a new [pull request](https://github.com/grammatek/tts-frontend/pulls).  