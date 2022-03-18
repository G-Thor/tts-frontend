"""

    TTS-text-process is a complete pipeline for preprocessing text for text-to-speech.

    Copyright (C) 2022 Grammatek ehf.

    This software is published under the Apache 2.0 License, sie LICENSE.
    Please note that submodules might be published under the MIT License (https://opensource.org/licenses/MIT)

    This is the entry point to the execution of the whole pipeline, single modules may be evoked from each
    manager (cleaner_manager, normalizer_manager, etc.). The main() function of this module is registered as
    a console_script entry point in setup.py

"""

from settings import ManagerResources
from settings import (
    HTML_CLOSING_TAG_REPL,
    PUNCTUATION,
    VALID_CHARACTERS,
)
from tts_tokenizer import Tokenizer
from tokens_manager import extract_text
from cleaner_manager import clean_text, clean_html_text, clean_html_string
from normalizer_manager import normalize_token_list
from phrasing_manager import phrase_token_list
from g2p_manager import transcribe


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
        """
        Clean 'text', ensuring only valid characters are included in the output. If 'html' is set to True,
        we assume the input text is in html-format, the processing method being implemented to parse
        html-epub-format for audio books.

        :param text: the input text to clean
        :param html: if True, the input text will be parsed as html and then cleaned
        :return: a list of CleanTokens representing a clean version of 'text'
        """
        if html:
            clean = clean_html_text(text, alphabet=self.get_alphabet(), punct_set=self.get_punct_symbols())
        else:
            clean = clean_text(text, alphabet=self.get_alphabet(), punct_set=self.get_punct_symbols())
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
        raw_text = text
        if html:
            raw_text = clean_html_string(text)
        clean = []
        tokenized = self.tokenizer.detect_sentences(raw_text)
        for sent in tokenized:
            clean.extend(self.clean(sent))
        normalized = normalize_token_list(clean)
        return normalized

    def phrase(self, text: str, html=False) -> list:
        """
        Normalizes 'text' and adds phrasing marks as pause tags ('<pau>' or '<sil>') to the normalized text.

        :param text: raw text or html-text to normalize and phrase
        :param html: if True, 'text' will be interpreted as html-string and parsed accordingly
        :return: a list of PhraseTokens representing a normalized version of 'text' with additional TagTokens representing
        ssml-tags or pauses. Includes processing history of each token.
        """
        normalized = self.normalize(text, html)
        phrased = phrase_token_list(normalized)
        return phrased

    def transcribe(self, text: str, html=False, phrasing=True, spellcheck=False, syllab_stress=False) -> list:
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

        transcribed = transcribe(normalized, syllab_stress)
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
    transcribed = manager.transcribe(input_text, syllab_stress=True)
    print('==========TRANSCRIBED=============')
    print(extract_text(transcribed, False))


if __name__ == '__main__':
    main()




