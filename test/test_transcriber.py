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

    def test_longer_text(self):
        manager = Manager()
        test_string = self.get_longer_text()
        transcribed = manager.transcribe(test_string, html=True)
        result_arr = manager.get_sentence_representation(transcribed, ignore_tags=False)
        self.assertEqual(3, len(result_arr))
        for sent in result_arr:
            print(sent)

    def test_longer_text_2(self):
        manager = Manager()
        test_string = self.get_longer_text_2()
        transcribed = manager.transcribe(test_string, phrasing=False)
        result_arr = manager.get_sentence_representation(transcribed, ignore_tags=False)
        self.assertEqual(10, len(result_arr))
        for sent in result_arr:
            print(sent)

    def get_custom_dict(self):
        custom = {'texti': 't_h E x s t I', 'engir': '9 N k v I r'}
        return custom

    def get_longer_text(self):
        return '<p id="hix00274"><span id="qitl_0591" class="sentence">Í kjölfarið sýndi hann fram á að það stuðli að ' \
               'heilbrigði ef einstaklingar geti fundið samhengi í tengslum við lífsatburði eða öðlast skilning á aðstæðum sínum. ' \
               '</span><span id="qitl_0592" class="sentence">Hann taldi uppsprettu heilbrigðis ' \
               '(e. </span><em><span id="qitl_0593" class="sentence">salutogenesis)</span></em><span id="qitl_0594" class="sentence"> ' \
               'vera að finna í mismunandi hæfni einstaklinga til að stjórna viðbrögðum sínum við álagi. </span>' \
               '<span id="qitl_0595" class="sentence">Antonovsky sýndi fram á að ef einstaklingar sem upplifðu álag sæju ' \
               'tilgang með reynslu sinni, þá þróaðist með þeim tilfinning fyrir samhengi í lífinu ' \
               '(e. </span><em><span id="qitl_0596" class="sentence">sense of coherence).</span></em>' \
               '<span id="qitl_0597" class="sentence"> Sigrún Gunnarsdóttir hefur íslenskað skilgreiningu hugtaksins ' \
               'um tilfinningu fyrir samhengi í lífinu á eftirfarandi hátt: </span></p>'

    def get_longer_text_2(self):
        return 'Þingflokkar allra stjórnarandstöðuflokkanna krefjast þess að Alþingi komi saman án tafar vegna nýrra ' \
               'vendinga í tengslum við söluna á hlut ríkisins í Íslandsbanka. Alþingi á samkvæmt dagskrá að koma saman ' \
               'til fundar á mánudag. Þingflokksformenn stjórnarandstöðuflokkanna segja hins vegar að málið þoli enga bið. ' \
               'Þingflokksformenn allra fimm stjórnarandstöðuflokkanna undirrita bréf sem þeir sendu forsætisráðherra ' \
               'og forseta Alþingis síðdegis. Þar segir að það sé ótækt að mál sem varða grundvallarhagsmuni þjóðarinnar ' \
               'séu leidd til lykta með fréttatilkynningum ríkisstjórnarinnar. ' \
               'Þar vísa þeir til þess að ríkisstjórnin tilkynnti í morgun að Bankasýsla ríkisins verði lögð niður. ' \
               'Með því var að hluta brugðist við gagnrýni sem beinst hefur að sölu á 22,5 prósenta hlut ríkisins í ' \
               'Íslandsbanka í síðasta mánuði. Þingmenn stjórnarandstöðu hafa í dag gagnrýnt ríkisstjórnina fyrir ' \
               'þögn undanfarinna daga og tilkynningu í dag um niðurlagningu Bankasýslunnar. Þrír þingmenn sögðu í ' \
               'hádegisfréttum að ráðamenn gætu ekki skotið sér undan ábyrgð á því hvernig salan á 22,5 prósenta hlut ' \
               'var framkvæmd. Það eru þau Þórhildur Sunna Ævarsdóttir, þingmaður Pírata, sem kallaði eftir afsögn ' \
               'fjármálaráðherra, Sigmar Guðmundsson, þingmaður Viðreisnar, sem sagði ríkisstjórnina reyna að nota ' \
               'Bankasýsluna sem skálkaskjól til að forðast að bera sjálf ábyrgð, og Kristrún Frostadóttir, sem sagði ' \
               'málinu alls ekki lokið og að það væri á ábyrgð fjármálaráðherra.'