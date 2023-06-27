import unittest
import os
from icefrontend import Frontend
import icefrontend.tokens_manager as tokens


class TestTokenizer(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.manager = Frontend()

    def setUp(self) -> None:
        self.manager.set_g2p_word_separator('')
        self.manager.set_g2p_syllab_symbol('')
        self.manager.set_g2p_custom_dict(None)

    def test_clean(self):
        manager = self.manager
        input_text = 'á bilinu 1,5-2,5%'
        result = manager.clean(input_text)
        result_str = tokens.extract_text(result)
        #print(str(result))
        #print(result_str)
        tokenized = manager.tokenize_from_list(result)
        print(str(tokenized))