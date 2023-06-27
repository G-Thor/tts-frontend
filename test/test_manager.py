import unittest
from icefrontend import Frontend


class TestManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.manager = Frontend()

    def setUp(self) -> None:
        self.manager.set_g2p_word_separator('')
        self.manager.set_g2p_syllab_symbol('')
        self.manager.set_g2p_custom_dict(None)


    def test_string_repr(self):
        manager = self.manager
        input_text = 'Snýst í suðaustan 10-18 m/s og hlýnar með rigningu'
        processed = manager.transcribe(input_text)
        result = manager.get_string_representation_normalized(processed)
        self.assertEqual('Snýst í suðaustan tíu til átján metrar á sekúndu og hlýnar með rigningu', result)
        transcribed = manager.get_string_representation_transcribed(processed)
        self.assertEqual('s t n i s t i: s Y: D 9i s t a n t_h i j Y t_h I: l au: t j au n m E: t r a r au: '
                         's E: k u n t Y O: G l_0 i: n a r m E: D r I k n i N k Y', transcribed)

    def test_stentence_repr(self):
        manager = self.manager
        input_text = 'Snýst í suðaustan 10-18 m/s og hlýnar með rigningu. Norðaustanátt og snjókoma NV-til fyrri part dags.'
        processed = manager.transcribe(input_text)
        result = manager.get_transcribed_sentence_representation(processed)
        self.assertEqual(2, len(result))

    def test_json_repr(self):
        manager = self.manager
        input_text = 'Snýst í suðaustan 10-18 m/s og hlýnar með rigningu'
        processed = manager.transcribe(input_text)
        result = manager.get_json_representation(processed)
        for elem in result:
            print(elem)
        self.assertEqual(11, len(result))