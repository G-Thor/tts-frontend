import unittest
import os
from src.manager.textprocessing_manager import Manager
import src.manager.tokens_manager as tokens


class TestNormalizer(unittest.TestCase):

    def test_normalize_weather(self):
        manager = Manager()
        input_text = '10-18 m/s'
        normalized = manager.normalize(input_text)
        result_str = tokens.extract_normalized_text(normalized)
        self.assertEqual('tíu til átján metrar á sekúndu', result_str)
        self.assertEqual('m/s', normalized[1].name)
        input_text = 'Snýst í suðaustan 10-18 m/s og hlýnar með rigningu, en norðaustanátt og snjókoma NV-til fyrri part dags.'
        normalized = manager.normalize(input_text, split_sent=False)
        result_str = tokens.extract_normalized_text(normalized, ignore_tags=False)
        self.assertEqual('Snýst í suðaustan tíu til átján metrar á sekúndu og hlýnar með rigningu <sil> en norðaustanátt og '
                         'snjókoma norðvestan til fyrri part dags <sentence>', result_str)
        self.assertEqual('NV-til', normalized[14].name)

    def test_normalize_denom(self):
        manager = Manager()
        input_text = '5/6'
        normalized = manager.normalize(input_text)
        result_str = tokens.extract_normalized_text(normalized)
        self.assertEqual('fimm sjöttu', result_str)
        input_text = '50 EUR/t og 3,5 millj./ha .'
        normalized = manager.normalize(input_text)
        result_str = tokens.extract_normalized_text(normalized)
        self.assertEqual('fimmtíu evrur á tonnið og þrjár komma fimm milljónir á hektarann', result_str)

    def test_normalize_abbr(self):
        manager = Manager()
        input_text = 'þetta voru ca. 5 mín.'
        normalized = manager.normalize(input_text)
        result_str = tokens.extract_normalized_text(normalized)
        self.assertEqual('þetta voru sirka fimm mínútur', result_str)
        input_text = '500 kwst.'
        normalized = manager.normalize(input_text)
        result_str = tokens.extract_normalized_text(normalized)
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
        result_str = tokens.extract_normalized_text(normalized)
        self.assertEqual('certainly kavity', result_str)

    def test_normalize_numbers(self):
        manager = Manager()
        input_text = 'Sími 570 2367 á sjúkrahúsinu'
        normalized = manager.normalize(input_text)
        result_str = tokens.extract_normalized_text(normalized)
        self.assertEqual('Sími fimm sjö núll <sil> tveir þrír sex sjö á sjúkrahúsinu', result_str)

    def test_normalize_acronyms(self):
        manager = Manager()
        input_text = 'Eins og FTSE vísitalan segir AIDS'
        normalized = manager.normalize(input_text)
        result_str = tokens.extract_normalized_text(normalized)
        print(result_str)
        self.assertEqual('Eins og F T S E vísitalan segir A I D S', result_str)

    def test_split_sentences(self):
        manager = Manager()
        input_text = self.get_long_text1()
        normalized = manager.normalize(input_text, split_sent=True)
        result_str = tokens.extract_normalized_text(normalized, ignore_tags=False)
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

    def test_split_sentences_to_list_2(self):
        manager = Manager()
        input_text = self.get_longer_text_2()
        normalized = manager.normalize(input_text, split_sent=True)
        result = manager.get_sentence_representation(normalized, ignore_tags=False)
        for sent in result:
            print(sent)
        self.assertEqual(10, len(result))

    def test_split_sentences_to_list_3(self):
        #TODO: fix 'kr. 156.459,-' (see Akranes_10.txt')
        manager = Manager()
        input_text = self.get_very_long_text()
        normalized = manager.normalize(input_text, split_sent=True)
        result = manager.get_sentence_representation(normalized, ignore_tags=False)
        print("no. of sentences: " + str(len(result)))
        for sent in result:
            print(sent)
        #self.assertEqual(10, len(result))

    def test_normalize_html(self):
        #TODO: fix 'kr. 156.459,-' (see Akranes_10.txt')
        manager = Manager()
        input_text = self.get_html_string()
        normalized = manager.normalize(input_text, html=True, split_sent=True)
        result = manager.get_sentence_representation(normalized, ignore_tags=False)
        print("no. of sentences: " + str(len(result)))
        for sent in result:
            print(sent)
        #self.assertEqual(10, len(result))


    def get_very_long_text(self):
        with open('../Akranes_10.txt') as f:
            return f.read()

    def get_long_text1(self):
        return 'Eins var þess krafðist að bankasölunni yrði rift. Að fundinum stóðu UNG ASÍ, Jæja hópurinn, Ungir Píratar, ' \
               'Ungir sósíalistar og Ungir jafnaðarmenn. Svalt var á Austurvelli í dag en hiti í fundarmönnum. '

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

    def get_html_string(self):
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

