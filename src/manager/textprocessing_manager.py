"""

    TTS-text-process is a complete pipeline for preprocessing text for text-to-speech.

    Copyright (C) 2022 Grammatek ehf.

    This software is published under the Apache 2.0 License, sie LICENSE.
    Please note that submodules might be published under the MIT License (https://opensource.org/licenses/MIT)

    This is the entry point to the execution of the whole pipeline, single modules may be evoked from each
    manager (cleaner_manager, normalizer_manager, etc.). The main() function of this module is registered as
    a console_script entry point in setup.py

"""

from .settings import ManagerResources
from .settings import (
    HTML_CLOSING_TAG_REPL,
    PUNCTUATION,
    VALID_CHARACTERS,
)
from .tts_tokenizer import Tokenizer
from .tokens_manager import extract_text
from .cleaner_manager import clean_text, clean_html_text
from .normalizer_manager import normalize_token_list
from .phrasing_manager import phrase_token_list
from .g2p_manager import transcribe

class Manager:

    def __init__(self):
        self.resources = ManagerResources()
        self.tokenizer = Tokenizer(self.get_abbreviations(), self.get_nonending_abbreviations())

    def get_abbreviations(self):
        return self.resources.abbreviations

    def get_nonending_abbreviations(self):
        return self.resources.nonending_abbreviations

    def get_prondict(self):
        return self.resources.pron_dict

    def get_alphabet(self):
        return VALID_CHARACTERS

    def get_punct_symbols(self):
        return PUNCTUATION

    def get_html_mapping(self):
        return HTML_CLOSING_TAG_REPL

    def clean(self, text: str, html=False) -> list:
        clean = text
        if html:
            clean = clean_html_text(text, alphabet=self.get_alphabet(), punct_set=self.get_punct_symbols())
        else:
            clean = clean_text(clean, alphabet=self.get_alphabet(), punct_set=self.get_punct_symbols())
        return clean

    def normalize(self, text: str) -> list:
        clean = []
        tokenized = self.tokenizer.detect_sentences(text)
        for sent in tokenized:
            clean.extend(self.clean(sent))
        normalized = normalize_token_list(clean)
        return normalized

    def phrase(self, text: str) -> list:
        normalized = self.normalize(text)
        phrased = phrase_token_list(normalized)
        return phrased

    def transcribe(self, text: str, phrasing=True, spellcheck=False) -> list:
        if phrasing:
            normalized = self.phrase(text)
        else:
            normalized = self.normalize(text)

        # TODO: add spellchecker manager
        if spellcheck:
            pass

        transcribed = transcribe(normalized)
        return transcribed


def main():
    input_text = 'Snýst í suðaustan 10-18 m/s og hlýnar með rigningu, en norðaustanátt og snjókoma NV-til fyrri part dags.'
    #input_text = 'að áramótum 2021/2022'
    manager = Manager()
    clean_input = manager.clean(input_text)
    print('==========CLEAN=============')
    print(extract_text(clean_input))
    normalized_input = manager.normalize(input_text)
    print('==========NORMALIZED=============')
    print(extract_text(normalized_input))
    phrased = manager.phrase(input_text)
    print('==========PHRASED=============')
    print(extract_text(phrased, False))
    transcribed = manager.transcribe(input_text)
    print('==========TRANSCRIBED=============')
    print(extract_text(transcribed, False))


if __name__ == '__main__':
    main()




