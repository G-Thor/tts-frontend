Badges

# TTS Textprocessing Pipeline for Icelandic

This project provides a TTS textprocessing pipeline for Icelandic. The pipeline includes modules for html parsing, text cleaning, text normalization for TTS, spell and grammar correction, phrasing, and grapheme-to-phoneme (g2p) conversion. Before a text can be fed into a TTS system it has to be converted into the format that was used when training that system. The format can be grapheme-based (i.e. alphabetic characters of the language in question are used as input) or phoneme-based (i.e. a phonetic alphabet like IPA or SAMPA are used as input). The TTS Textprocessing Pipeline for Icelandic offers both possibilities.

## The Pipeline

The TTS frontend pipeline makes seamless text preprocessing for TTS using different submodules possible. It manages tags, e.g. SSML tags, that might be added or processed at different stages, and stores the processing history of each token from original input, through normalizing and correction to phonetic representation at the end of the pipeline.

## Prerequisites and setup
Assuming you have Python > 3.6 installed, create a virtual environment, e.g.

This project is in a development state, as the subodules as well, and thus a PyPI package does not yet exist.
You can install the project either by cloning the repository and install from the project root, or you can install
directly from github:

```
$ # clone and install:
$ git clone https://github.com/grammatek/tts-frontend.git
$ cd tts-frontend
$ # create a virtual env
$ python3 -m venv <path/to/your/venv>
$ source <path/to/your/venv>/bin/activate
(venv) $ pip install -e .
```

**NOTE:** The setup works with `pip 21.3.1` , upgrading pip to a newer version caused fairseq
installation to fail (see unresolved issue here: https://github.com/pytorch/fairseq/issues/3535)

## Usage
How to use the project

## Credits
Máltækniáætlun, devleopers of submodules

## License

## Contributing / Contact