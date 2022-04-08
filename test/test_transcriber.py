import unittest
import os
from src.manager.textprocessing_manager import Manager
import src.manager.tokens_manager as tokens


class TestNormalizer(unittest.TestCase):

    def test_simple_transcript(self):
        manager = Manager()
        input_text = 'hlaupa'
        transcribed = manager.transcribe(input_text)
        result_str = tokens.extract_text(transcribed)
        self.assertEqual('l_0 9i: p a', result_str)

    def test_word_sep_transcribe(self):
        manager = Manager()
        manager.set_g2p_word_separator('-')
        test_string = 'hlaupa í burtu í dag'
        transcribed = manager.transcribe(test_string)
        result_str = tokens.extract_text(transcribed, word_separator='-')
        self.assertEqual('l_0 9i: p a - i: - p Y r_0 t Y - i: - t a: G', result_str)

    def test_syllabification(self):
        manager = Manager()
        manager.set_g2p_syllab_symbol('.')
        test_string = 'hlaupa í burtu í dag'
        transcribed = manager.transcribe(test_string)
        result_str = tokens.extract_text(transcribed)
        self.assertEqual('l_0 9i: . p a i: p Y r_0 . t Y i: t a: G', result_str)

    def test_custom_dict(self):
        manager = Manager()
        custom_dict = self.get_custom_dict()
        manager.set_g2p_custom_dict(custom_dict)
        test_string = 'þessi texti en engir aukvisar'
        transcribed = manager.transcribe(test_string)
        result_str = tokens.extract_text(transcribed)
        self.assertEqual('T E s I t_h E x s t I E n 9 N k v I r 9i: k v I s a r', result_str)

    def get_custom_dict(self):
        custom = {'texti': 't_h E x s t I', 'engir': '9 N k v I r'}
        return custom
