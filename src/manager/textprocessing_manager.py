"""

    TTS-text-process is a complete pipeline for preprocessing text for text-to-speech.

    Copyright (C) 2022 Grammatek ehf.

    This software is published under the Apache 2.0 License, sie LICENSE.
    Please note that submodules might be published under the MIT License (https://opensource.org/licenses/MIT)

    This is the entry point to the execution of the whole pipeline, single modules may be evoked from each
    manager (cleaner_manager, normalizer_manager, etc.), but this module also contains methods to run single
    modules or a part of the pipeline. The main() function of this module is registered as
    a console_script entry point in setup.py

"""
import argparse

from .unicode_maps import replacement_dictionary, post_dict_lookup
from .settings import ManagerResources
from .settings import (
    HTML_CLOSING_TAG_REPL,
    PUNCTUATION,
    VALID_CHARACTERS,
)
from .tts_tokenizer import Tokenizer
from .tokens_manager import extract_text, align_tokens
from .cleaner_manager import CleanerManager
from .normalizer_manager import NormalizerManager
from .phrasing_manager import PhrasingManager
from .g2p_manager import G2PManager


class Manager:

    def __init__(self, custom_pron_dict={}):
        self.resources = ManagerResources()
        self.tokenizer = Tokenizer(self.get_abbreviations(), self.get_nonending_abbreviations())
        cleaner_lexicon = self.get_default_cleaner_lexicon()
        self.cleaner = CleanerManager(self.get_replacement_dict(), self.get_post_lookup_dict(), cleaner_lexicon)
        self.normalizer = NormalizerManager()
        self.phrasing = PhrasingManager()
        self.g2p = G2PManager()
        self.g2p.set_custom_dict(custom_pron_dict)

    def get_abbreviations(self):
        return self.resources.abbreviations

    def get_nonending_abbreviations(self):
        return self.resources.nonending_abbreviations

    def get_prondict(self):
        return self.resources.pron_dict

    def get_replacement_dict(self):
        return replacement_dictionary

    def get_post_lookup_dict(self):
        return post_dict_lookup

    def get_alphabet(self):
        return VALID_CHARACTERS

    def get_punct_symbols(self):
        return PUNCTUATION

    def get_html_mapping(self):
        return HTML_CLOSING_TAG_REPL

    def get_default_cleaner_lexicon(self) -> list:
        lexicon = list(self.get_prondict().keys())
        lexicon.extend(self.get_abbreviations())
        lexicon.extend(self.get_nonending_abbreviations())
        return lexicon

    def set_g2p_custom_dict(self, pron_dict: dict):
        self.g2p.set_custom_dict(pron_dict)

    def set_g2p_syllab_symbol(self, syllab_symbol: str):
        self.g2p.set_syllab_symbol(syllab_symbol)

    def set_g2p_stress(self, value: bool):
        self.g2p.set_stress(value)

    def set_g2p_word_separator(self, word_sep: str):
        self.g2p.set_word_separator(word_sep)

    def clean(self, text: str, html=False) -> list:
        """
        Clean 'text', ensuring only valid characters are included in the output. If 'html' is set to True,
        we assume the input text is in html-format, the processing method being implemented to parse
        html-epub-format for audio books.

        :param text: the input text to clean
        :param html: if True, the input text will be parsed as html and then cleaned
        :return: a list of CleanTokens representing a clean version of 'text'
        """
        if html:
            clean = self.cleaner.clean_html_text(text)
        else:
            clean = self.cleaner.clean_text(text)
        return clean

    def normalize(self, text: str, html=False) -> list:
        """
        Normalize 'text', ensuring it does not contain any characters or symbols not valid for g2p.

        :param text: raw text or html-text to normalize
        :param html: if True, 'text' will be interpreted as html-string and parsed accordingly
        :return: a list or NormalizedTokens representing a normalized version of 'text' with additional TagTokens representing
        ssml-tags or pauses. Includes processing history of each token.
        of each token
        """
        clean = self.clean(text, html)
        tokenized = self.tokenizer.detect_sentences(extract_text(clean))
        clean_tokenized = align_tokens(clean, tokenized)
        normalized = self.normalizer.normalize_token_list(clean_tokenized)
        normalized_with_tag_tokens = self.phrasing.add_pause_tags(normalized)
        return normalized_with_tag_tokens

    def phrase(self, text: str, html=False) -> list:
        """
        Normalizes 'text' and adds phrasing marks as pause tags ('<pau>' or '<sil>') to the normalized text.

        :param text: raw text or html-text to normalize and phrase
        :param html: if True, 'text' will be interpreted as html-string and parsed accordingly
        :return: a list of PhraseTokens representing a normalized version of 'text' with additional TagTokens representing
        ssml-tags or pauses. Includes processing history of each token.
        """
        normalized = self.normalize(text, html)
        phrased = self.phrasing.phrase_token_list(normalized)
        return phrased

    def transcribe(self, text: str, html=False, phrasing=True, spellcheck=False) -> list:
        """
        Transcribes 'text' using the SAMPA phonetic alphabet.

        :param text: raw text or html-text to transcribe
        :param html: if True, 'text' will be interpreted as html-string and parsed accordingly
        :param phrasing: if True, perform phrasing after normalizing (and spellcheck if applied)
        :param spellcheck: if True, perform spellcheck after normalizing
        :param syllab_stress: if True, add syllabification and stress labels to the phonetic transcripts
        :return: a list of TranscribedTokens representing a transcribed version of 'text' with additional TagTokens representing
        ssml-tags or pauses. Includes processing history of each token.
        """
        if phrasing:
            normalized = self.phrase(text, html)
        else:
            normalized = self.normalize(text, html)

        # TODO: add spellchecker manager
        if spellcheck:
            pass

        transcribed = self.g2p.transcribe(normalized)
        return transcribed


def parse_args():
    parser = argparse.ArgumentParser(description='tts frontend-pipeline for raw text')
    parser.add_argument('input_text', type=str, help='text to process for tts')

    return parser.parse_args()


def main():
    input_text1 = 'Snýst í suðaustan 10-18 m/s og hlýnar með rigningu, en norðaustanátt og snjókoma NV-til fyrri part dags.'
    input_text = 'Sími 570 4509'

    #args = parse_args()
    #if not args.input_text:
    #    print('please provede string to process!')
    #    exit()

    #input_text = args.input_text
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
    manager.set_g2p_syllab_symbol('.')
    transcribed = manager.transcribe(input_text, phrasing=False)
    print('==========TRANSCRIBED=============')
    print(extract_text(transcribed, False))


if __name__ == '__main__':
    main()




