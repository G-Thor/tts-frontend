import unittest
import os
from src.manager.textprocessing_manager import Manager
import src.manager.tokens_manager as tokens


class TestNormalizer(unittest.TestCase):

    def test_normalize_weather(self):
        manager = Manager()
        input_text = '10-18 m/s'
        normalized = manager.normalize(input_text)
        result_str = tokens.extract_text(normalized)
        self.assertEqual('tíu til átján metrar á sekúndu', result_str)
        self.assertEqual('m/s', normalized[5].original_token.name)
        input_text = 'Snýst í suðaustan 10-18 m/s og hlýnar með rigningu, en norðaustanátt og snjókoma NV-til fyrri part dags.'
        normalized = manager.normalize(input_text, split_sent=False)
        result_str = tokens.extract_text(normalized, ignore_tags=False)
        self.assertEqual('Snýst í suðaustan tíu til átján metrar á sekúndu og hlýnar með rigningu <sil> en norðaustanátt og '
                         'snjókoma norðvestan til fyrri part dags', result_str)
        self.assertEqual('NV-til', normalized[19].original_token.name)

    def test_normalize_denom(self):
        manager = Manager()
        input_text = '5/6'
        normalized = manager.normalize(input_text)
        result_str = tokens.extract_text(normalized)
        self.assertEqual('fimm sjöttu', result_str)
        input_text = '50 EUR/t og 3,5 millj./ha .'
        normalized = manager.normalize(input_text)
        result_str = tokens.extract_text(normalized)
        self.assertEqual('fimmtíu evrur á tonnið og þrjár komma fimm milljónir á hektarann', result_str)

    def test_normalize_abbr(self):
        manager = Manager()
        input_text = 'þetta voru ca. 5 mín.'
        normalized = manager.normalize(input_text)
        result_str = tokens.extract_text(normalized)
        self.assertEqual('þetta voru sirka fimm mínútur', result_str)
        input_text = '500 kwst.'
        normalized = manager.normalize(input_text)
        result_str = tokens.extract_text(normalized)
        #normalizer does not normalize kwst. correctly, has to do with upper and lower case
        #TODO: fix in normalizer
        #self.assertEqual('fimm hundruð kílóvattstundir', result_str)

    def test_normalize_foreign(self):
        manager = Manager()
        input_text = 'the wall'
        normalized = manager.normalize(input_text)
        result_str = tokens.extract_text(normalized)
        self.assertEqual('the wall', result_str)
        input_text = 'certainly cawity'
        normalized = manager.normalize(input_text)
        result_str = tokens.extract_text(normalized)
        self.assertEqual('certainly kavity', result_str)

    def test_normalize_numbers(self):
        manager = Manager()
        input_text = 'Sími 570 2367'
        normalized = manager.normalize(input_text)
        result_str = tokens.extract_text(normalized)
        self.assertEqual('Sími fimm sjö núll <sil> tveir þrír sex sjö', result_str)

    def test_split_sentences(self):
        manager = Manager()
        input_text = self.get_long_text1()
        normalized = manager.normalize(input_text, split_sent=True)
        result_str = tokens.extract_text(normalized, ignore_tags=False)
        self.assertEqual('Eins var þess krafðist að bankasölunni yrði rift <sentence> Að fundinum stóðu U N G A S Í <sil> '
                         'Jæja hópurinn <sil> '
                         'Ungir Píratar <sil> Ungir sósíalistar og Ungir jafnaðarmenn <sentence> '
                         'Svalt var á Austurvelli í dag en hiti '
                         'í fundarmönnum <sentence>', result_str)

    def test_split_sentences_to_list(self):
        manager = Manager()
        input_text = self.get_long_text1()
        normalized = manager.normalize(input_text, split_sent=True)
        result = manager.get_sentence_representation(normalized, ignore_tags=False)
        #for sent in result:
        #    print(sent)
        self.assertEqual(3, len(result))


    def get_long_text1(self):
        return 'Eins var þess krafðist að bankasölunni yrði rift. Að fundinum stóðu UNG ASÍ, Jæja hópurinn, Ungir Píratar, ' \
               'Ungir sósíalistar og Ungir jafnaðarmenn. Svalt var á Austurvelli í dag en hiti í fundarmönnum. '

