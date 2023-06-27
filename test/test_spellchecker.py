import unittest
import os
from icefrontend import Frontend
import icefrontend.tokens_manager as tokens

class TestSpellchecker(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.manager = Frontend()

    def setUp(self) -> None:
        self.manager.set_g2p_word_separator('')
        self.manager.set_g2p_syllab_symbol('')
        self.manager.set_g2p_custom_dict(None)


    def test_spellcheck1(self):
        manager = self.manager
        input_text = 'Ég vil hríngja í 557 1234'
        transcribed = manager.transcribe(input_text, spellcheck=True)
        result_str = tokens.extract_transcribed_text(transcribed, ignore_tags=False)
        print(result_str)
        self.assertEqual('j E: G v I: l r_0 i J c a i: f I m f I m s j 9: <sil> '
                         'ei t n_0 t_h v ei: r T r i: r f j ou: r I r <sentence>',
                         result_str)

    def test_spellcheck2(self):
        manager = self.manager
        input_text = 'Ég vil hríngja í 557 1234, það er símin hja Guðmund'
        transcribed = manager.transcribe(input_text, spellcheck=True)
        result_str = tokens.extract_transcribed_text(transcribed, ignore_tags=False)
        print(result_str)
        self.assertEqual('j E: G v I: l r_0 i J c a i: f I m f I m s j 9: <sil> ei t n_0 t_h v ei: r T '
                            'r i: r f j ou: r I r <sil> T a: D <sil> E r s i: m I n C au: k v Y D m Y n t <sentence>',
                         result_str)