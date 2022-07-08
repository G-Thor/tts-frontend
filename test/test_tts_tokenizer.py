import unittest
import os
from manager.textprocessing_manager import Manager
import manager.tokens_manager as tokens


class TestTokenizer(unittest.TestCase):

    def test_clean(self):
        manager = Manager()
        input_text = 'á bilinu 1,5-2,5%'
        result = manager.clean(input_text)
        result_str = tokens.extract_text(result)
        #print(str(result))
        #print(result_str)
        tokenized = manager.tokenize_from_list(result)
        print(str(tokenized))