import unittest
import pprint
from manager.textprocessing_manager import Manager


class TestManager(unittest.TestCase):

    def test_string_repr(self):
        manager = Manager()
        input_text = 'Snýst í suðaustan 10-18 m/s og hlýnar með rigningu'
        processed = manager.transcribe(input_text)
        result = manager.get_string_representation_normalized(processed)
        self.assertEqual('Snýst í suðaustan tíu til átján metrar á sekúndu og hlýnar með rigningu', result)
        transcribed = manager.get_string_representation_transcribed(processed)
        self.assertEqual('s t n i s t i: s Y: D 9i s t a n t_h i j Y t_h I: l au: t j au n m E: t r a r au: '
                         's E: k u n t Y O: G l_0 i: n a r m E: D r I k n i N k Y', transcribed)

    def test_stentence_repr(self):
        manager = Manager()
        input_text = 'Snýst í suðaustan 10-18 m/s og hlýnar með rigningu. Norðaustanátt og snjókoma NV-til fyrri part dags.'
        processed = manager.transcribe(input_text)
        result = manager.get_transcribed_sentence_representation(processed)
        self.assertEqual(2, len(result))

    def test_json_repr(self):
        manager = Manager()
        input_text = 'Snýst í suðaustan 10-18 m/s og hlýnar með rigningu'
        processed = manager.transcribe(input_text)
        result = manager.get_json_representation(processed)
        for elem in result:
            pprint.pprint(elem)
        self.assertEqual(11, len(result))