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

import time

from unicode_maps import replacement_dictionary, post_dict_lookup
from settings import ManagerResources
from settings import (
    HTML_CLOSING_TAG_REPL,
    PUNCTUATION,
    VALID_CHARACTERS,
)
from tts_tokenizer import Tokenizer
from tokens_manager import extract_text, align_tokens
from cleaner_manager import CleanerManager
from normalizer_manager import NormalizerManager
from phrasing_manager import PhrasingManager
from g2p_manager import G2PManager


class Manager:

    def __init__(self):
        self.resources = ManagerResources()
        self.tokenizer = Tokenizer(self.get_abbreviations(), self.get_nonending_abbreviations())
        self.cleaner = CleanerManager(self.get_replacement_dict(), self.get_post_lookup_dict())
        self.normalizer = NormalizerManager()
        self.phrasing = PhrasingManager()
        self.g2p = G2PManager()

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

    def set_g2p_syllab_stress(self, value: bool):
        self.g2p.set_syllab_stress(value)

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
    #input_text = 'Snýst í suðaustan 10-18 m/s og hlýnar með rigningu, en norðaustanátt og snjókoma NV-til fyrri part dags.'
    input_text1 = 'Anna Guðný Guðmundsdóttir, píanóleikari, fæddist 6. september 1958 í Reykjavík og ólst upp á Háaleitisbraut. Hún var í sveit í fimm ár að Fagurhólsmýri í Öræfunum, rétt áður en síðustu árnar voru brúaðar og hringvegurinn var kláraður. Þar var hún kúarektor, sinnti bústörfum, afgreiddi bensín og spilaði Bach á gamalt fótstigið orgel. ' \
                 'Anna Guðný hóf snemma píanónám í Barnamúsíkskólanum hjá Stefáni Edelstein, gekk í Álftamýrarskóla og lauk stúdentsprófi frá Menntaskólanum við Hamrahlíð 1977. Því næst lauk Anna burtfararprófi frá Tónlistarskólanum í Reykjavík 1979, þar sem Hermína S. Kristjánsson, Jón Nordal og Margrét Eiríksdóttir voru meðal hennar leiðbeinenda. Loks lauk Anna Post Graduate Diploma frá Guildhall School of Music and Drama í London árið 1982. Anna Guðný lagði sérstaka áherslu á kammermúsík og meðleik með söng og þar hófst farsælt samstarf hennar og söngkonunnar Sigrúnar Hjálmtýsdóttur, Diddú. Anna Guðný sótti námskeið og einkatíma hjá Erik Werba, Rudolf Jansen, György Sebök, John Lill og fleiri kennurum. ' \
                 'Um langt árabil hefur Anna Guðný sinnt kennstustörfum, var píanókennari við Tónlistarskólann í Reykjavík og einnig við Menntaskólann í tónlist. Hún var lausráðin píanóleikari með Sinfóníuhljómsveit Íslands frá 1985, var í Íslensku hljómsveitinni 1982 til 1990 og Kammersveit Reykjavíkur frá 1982. Hún var meðleikari við tónlistardeild Listaháskóla Íslands frá 2001 til 2005, en hefur verið frá því þá fastráðin hjá Sinfóníuhljómsveit Íslands. ' \
                 'Anna Guðný hefur víða komið fram á sínum glæsta ferli; fjölda kammertónleika með ýmsum söngvurum og hljóðfæraleikurum, á vegum Kammermúsíkklúbbsins, í Tíbrá tónleikaröðinni, sem einleikari á Sinfóníutónleikum og tekið þátt í tónlistarhátíðum um allt land. Anna Guðný hefur einnig leikið á tónleikum um mestalla Evrópu, Kína, Japan, á Norðurlöndunum og víðar. Að auki hefur hún spilað inn á um 30 hljómplötur með ýmsum listamönnum og gefið út rómaðar einleiksplötur. ' \
                 'Anna Guðný hefur þrisvar verið tilnefnd til Íslensku tónlistarverðlaunanna og hlaut verðlaunin árið 2008, sem flytjandi ársins, fyrir heildarflutning á tónverkinu Tuttugu tillit til Jesúbarnsins eftir Oliver Messiaen. Hún hlaut starfslaun menntamálaráðuneytisins 1995 og 2000, hlaut orðu Hvítu rósarinnar frá finnska ríkinu 1997, hún hefur sinnt tónlistarráðgjöf á safninu á Gljúfrasteini um árabil og var bæjarlistamaður Mosfellsbæjar 2002. Hún er og hefur verið mikilvægur og sterkur hlekkur í íslensku tónlistarlífi í fjóra áratugi. ' \
                 'Anna Guðný Guðmundsdóttir er handhafi heiðursverðlauna Íslensku tónlistarverðlaunanna árið 2022. „Ég hef verið umvafin tónlist frá því ég man eftir mér og það hefur verið mín gæfa. Ég trúi því að sá sem lifir í tónlist þurfi aldrei að vera einmana, verkefnalaus og vinalaus,“ sagði hún meðal annars í ræðu sinni. Hún hefur stigið til hliðar vegna veikinda en þakkar þeim sem hafa átt samleið með henni í gegnum árin. „Tónlistin getur bæði sefað og sameinað. Takk fyrir mig,“ voru lokaorð hennar.'

    input_text = 'einmana, verkefnalaus og vinalaus,“ sagði hún' # phrasing res: 'einmana' 'verkefnalaus' '<pau>' 'og' 'vinalaus<pau><sp>' 'sagði' 'hún'
    test_sent2 = 'Reykjavíkur frá 1982. Hún var meðleikari' # need to split the dot after the year digit, if followed by an upper case letter
    print('tokens in input: ' + str(len(input_text.split())))
    #args = parse_args()
    #if not args.input_text:
    #    print('please provede string to process!')
    #    exit()

    #input_text = args.input_text
    manager = Manager()
    start1 = time.time()
    clean_input = manager.clean(input_text)
    print('==========CLEAN=============')
    print(extract_text(clean_input))
    start2 = time.time()
    normalized_input = manager.normalize(input_text)
    print('==========NORMALIZED=============')
    print(extract_text(normalized_input))
    start3 = time.time()
    phrased = manager.phrase(input_text)
    print('==========PHRASED=============')
    print(extract_text(phrased, False))
    start4 = time.time()
    manager.set_g2p_syllab_stress(True)
    transcribed = manager.transcribe(input_text, phrasing=False)
    print('==========TRANSCRIBED=============')
    print(extract_text(transcribed, False))
    start5 = time.time()

    print('CLEAN: ' + str(start2 - start1))
    print('NORMALIZE: ' + str(start3 - start2))
    print('PHRASE: ' + str(start4 - start3))
    print('TRANSCRIBE: ' + str(start5 - start4))


if __name__ == '__main__':
    main()




