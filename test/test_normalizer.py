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
        for elem in normalized:
            print(elem.to_json())

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
        input_text = 'Síminn er 570 2367 á sjúkrahúsinu'
        normalized = manager.normalize(input_text)
        result_str = tokens.extract_normalized_text(normalized)
        self.assertEqual('Síminn er fimm sjö núll <sil> tveir þrír sex sjö á sjúkrahúsinu', result_str)

    def test_normalize_acronyms(self):
        manager = Manager()
        input_text = 'Eins og FTSE vísitalan segir AIDS'
        normalized = manager.normalize(input_text)
        result_str = tokens.extract_normalized_text(normalized)
        print(result_str)
        self.assertEqual('Eins og F T S E vísitalan segir AIDS', result_str)

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

    def test_percent(self):
        manager = Manager()
        input_text = '1,5-2,5%'
        normalized = manager.normalize(input_text)
        result_str = tokens.extract_normalized_text(normalized)
        self.assertEqual('eitt komma fimm til tvö komma fimm prósent', result_str)

    def test_hyphen(self):
        manager = Manager()
        input_text = 'Blikar heppnir, KR-ingar óheppnir.'
        normalized = manager.normalize(input_text)
        result_str = tokens.extract_normalized_text(normalized, ignore_tags=False)
        self.assertEqual('Blikar heppnir <sil> K R  <sil> ingar <sil> óheppnir <sentence>', result_str)
        input_text = 'Evrópa (EFTA-ríkin)'
        normalized = manager.normalize(input_text)
        result_str = tokens.extract_normalized_text(normalized, ignore_tags=False)
        # TODO: fix space issue in normalizer
        self.assertEqual('Evrópa <sil> EFTA <sil> ríkin <sentence>', result_str)
        # TODO: fix space issue in normalizer

        input_text = 'EFTA-ríkin'
        normalized = manager.normalize(input_text)
        result_str = tokens.extract_normalized_text(normalized)
        # TODO: fix space issue in normalizer
        self.assertEqual('EFTA  <sil> ríkin', result_str)
        input_text = 'Evrópa (EFTA-ríkin)'
        normalized = manager.normalize(input_text)
        result_str = tokens.extract_normalized_text(normalized, ignore_tags=False)
        # TODO: fix space issue in normalizer
        self.assertEqual('Evrópa <sil> EFTA <sil> ríkin <sentence>', result_str)

    def test_sport_results_time(self):
        manager = Manager()
        input_text = '100 metra bringusundi S14 þroskahamlaðra á 1:09,14 mínútu og var örskammt frá Íslandsmeti sínu ' \
                     'í greininni sem er 1:09,01 mínúta.'
        normalized = manager.normalize(input_text)
        result_str = tokens.extract_normalized_text(normalized, ignore_tags=False)
        print(result_str)
        #self.assertEqual('hundrað metra bringusundi S fjórtán þroskahamlaðra á '
        #            'einni núll níu komma fjórtán mínútu og var örskammt frá Íslandsmeti sínu í greininni sem er ein núll '
        #            'níu komma núll ein mínúta.', result_str)

    def test_born_dead(self):
        manager = Manager()
        input_text = 'Jón, f. 4. apríl 1927, d. 10. febrúar 2010.'
        normalized = manager.normalize(input_text)
        result_str = tokens.extract_normalized_text(normalized, ignore_tags=False)
        self.assertEqual('Jón <sil> fæddur fjórða apríl nítján hundruð tuttugu og sjö <sil>'
                         ' dáinn tíunda febrúar tvö þúsund og tíu <sentence>', result_str)

    def test_digits(self):
        manager = Manager()
        input_text = 'Blálanga, óslægð 10.6.22 130,00 kr/kg. Er lagt til að ákvæðið gildi til 31. maí 2023.'
        normalized = manager.normalize(input_text)
        result_str = tokens.extract_normalized_text(normalized, ignore_tags=False)
        print(result_str)
       # self.assertEqual('Blálanga <sil> óslægð tíunda sjötta tuttugu og tvö hundrað og þrjátíu krónur'
       #                  ' á kílóið <sentence> Er lagt til að ákvæðið gildi til þrítugasta og fyrsta'
       #                  ' maí tvö þúsund tuttugu og þrjú <sentence>', result_str)

    def test_year_digits(self):
        manager = Manager()
        input_text = 'síðan í mars 2010. mbl.is/​ Kristinn Magnússon'
        normalized = manager.normalize(input_text)
        result_str = tokens.extract_normalized_text(normalized, ignore_tags=False)
        self.assertEqual('síðan í mars tvö þúsund og tíu <sil> m b l punktur i s <sil> Kristinn Magnússon <sentence>', result_str)

    def test_year_digits_and_percent(self):
        manager = Manager()
        input_text = 'Í nýrri verðbólguspá Greiningar Íslandsbanka er því spáð að vísitala neysluverðs hækki um 1% í júní. ' \
                    'Gangi spáin eftir mælist 12 mánaða verðbóla 8,4%, en hún hefur ekki mælst svo mikil síðan í mars ' \
                    '2010. mbl.is/​ Kristinn Magnússon'
        normalized = manager.normalize(input_text)
        result_str = tokens.extract_normalized_text(normalized, ignore_tags=False)
        self.assertEqual('Í nýrri verðbólguspá Greiningar Íslandsbanka er því spáð að vísitala neysluverðs hækki um eitt prósent í júní'
                         ' <sentence> '
                    'Gangi spáin eftir mælist tólf mánaða verðbóla átta komma fjögur prósent <sil> en hún hefur ekki mælst svo mikil síðan í mars '
                    'tvö þúsund og tíu <sil> m b l punktur i s <sil> Kristinn Magnússon <sentence>',
                result_str)

    def test_normalize_div(self):
        manager = Manager()
        test_map = self.get_test_map()
        for elem in test_map:
            normalized = manager.normalize(elem, split_sent=True)
            norm_text = tokens.extract_normalized_text(normalized)
            #self.assertEqual(norm_text, test_map[elem])

    def test_normalize_hbs_text(self):
        manager = Manager()
        test_list = self.get_hbs_test_list()
        for elem in test_list:
            normalized = manager.normalize(elem, split_sent=True)
            norm_text = tokens.extract_normalized_text(normalized, ignore_tags=False)
            print(norm_text)

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

    def get_test_map(self):
        test_map = {'Í Evrópu hélt lækkunin áfram þar sem markaðir lækkuðu á bilinu 1,5-2,5%' :
                    'Í Evrópu hélt lækkunin áfram þar sem markaðir lækkuðu á bilinu eitt komma fimm til tvö komma fimm prósent',
                    'Fríverslunarsamtaka Evrópu (EFTA-ríkin).' : 'Fríverslunarsamtaka Evrópu efta ríkin',
                    '100 metra bringusundi S14 þroskahamlaðra á 1:09,14 mínútu og var örskammt frá Íslandsmeti sínu '
                     'í greininni sem er 1:09,01 mínúta.' : 'hundrað metra bringusundi S fjórtán þroskahamlaðra á '
                    'einni núll níu komma fjórtán mínútu og var örskammt frá Íslandsmeti sínu í greininni sem er ein núll '
                    'níu komma núll ein mínúta.',
                    'Foreldrar hans voru Jóna Einarsdóttir húsfreyja frá Túni á Eyrarbakka, f. 4. apríl 1927, d. 10. febrúar 2010.'  :
                    'Foreldrar hans voru Jóna Einarsdóttir húsfreyja frá Túni á Eyrarbakka <sil> fædd fjórða apríl '
                    'nítján hundruð tuttugu og sjö <sil> dáin tíunda febrúar tvö þúsund og tíu',
                    'Blikar heppnir, KR-ingar óheppnir.' : 'Blikar heppnir <sil> K R ingar óheppnir',
                    'Blálanga, óslægð 10.6.22 130,00 kr/kg. Er lagt til að ákvæðið gildi til 31. maí 2023.' :
                    'Blálanga <sil> óslægð tíunda júní tuttugu og tvö hundrað og þrjátíu krónur á kílóið Er lagt til '
                    'að ákvæðið gildi til þrítugasta og fyrsta maí tvö þúsund tuttugu og þrjú',
                    'Í nýrri verðbólguspá Greiningar Íslandsbanka er því spáð að vísitala neysluverðs hækki um 1% í júní. '
                    'Gangi spáin eftir mælist 12 mánaða verðbóla 8,4%, en hún hefur ekki mælst svo mikil síðan í mars '
                    '2010. mbl.is/​ Kristinn Magnússon' :
                    'Í nýrri verðbólguspá Greiningar Íslandsbanka er því spáð að vísitala neysluverðs hækki um eitt prósent í júní '
                    'Gangi spáin eftir mælist tólf mánaða verðbóla átta komma fjögur prósent <sil> en hún hefur ekki mælst '
                    'svo mikil síðan í mars tvö þúsund og tíu . m b l punktur is <sil> Kristinn Magnússon'}
        return test_map

    def get_hbs_test_list(self):
        test_map = ['Prufuskjal fyrir talgervil',
                        'Hljóðstafir - Stutt verkefnislýsing',
                        'Tilgangur verkefnisins:',
                        'Í nýrri verðbólguspá Greiningar Íslandsbanka er því spáð að vísitala neysluverðs hækki um 1% í júní. '
                        'Gangi spáin eftir mælist 12 mánaða verðbóla 8,4%, en hún hefur ekki mælst svo mikil síðan í mars '
                        '2010. mbl.is/​ Kristinn Magnússon',
                        'Hugbúnaðarfyrirtækið ExMon Software hefur vaxið hratt.',
                        'Blálanga, óslægð 10.6.22 130,00 kr/kg. Er lagt til að ákvæðið gildi til 31. maí 2023.',
                        'Húrra!',
                        'Blikar heppnir, KR-ingar óheppnir.',
                        'Samtals 1.707 kg',
                        'Róbert og Thelma komin í úrslit á HM.',
                        'Hedwig Franziska Elisabeth Meyer fæddist í Rechterfeld í Niedersachsen-héraði í Þýskalandi 25.',
                        'Foreldrar hans voru Jóna Einarsdóttir húsfreyja frá Túni á Eyrarbakka, f. 4. apríl 1927, d. 10. febrúar 2010.',
                        '100 metra bringusundi S14 þroskahamlaðra á 1:09,14 mínútu og var örskammt frá Íslandsmeti sínu '
                        'í greininni sem er 1:09,01 mínúta.',
                        'Fríverslunarsamtaka Evrópu (EFTA-ríkin).',
                        '„Ég hef verið á Skriðuklaustri frá 1999 og stýrt uppbyggingu á rithöfundasafni.',
                        'Í Evrópu hélt lækkunin áfram þar sem markaðir lækkuðu á bilinu 1,5-2,5%.',
                        '2. Veita útgefendum aðgang að kerfi þar sem þeir geta tekið texta og hljóð sem eru formuð '
                        'eftir skilgreiningu HBS (sem byggir á alþjóðastöðlum) og sett saman sem aðgengilega bók með texta.',
                        'Kaupa flokkunar- og pökkunarlínu frá Micro.',
                        '13.6.22 Sæfinnur EA-058.',
                        'Fríverslunarsamningi EFTA-ríkjanna og Úkraínu.',
                        'Þá mun samruninn verða framkvæmdur á þeim grundvelli að SalMar er kaupandi allra hluta í NRS '
                        'og eru greiddir 0,369 hlutir í SalMar fyrir hvern hlut í NRS.',
                        'Hversu margar bækur þarf?',
                        'Þurfa að vera öðruvísi, hvort sem er tungumál, hraði á lestri, gæði á hljóðfælum, allskonar '
                        'edge-case, til að ná að tvíka og laga og gera sjálfvirkt.',
                        'Gætum byrjað á Harry Potter',
                        'Öll flækjustig bóka í upphafi eða byrja á einfaldari bókum?',
                        'Kennslubækur með myndir, lestur ekki 100% línulaga, horizontal lesið, upp og niður allsstaðar '
                        'í gegnum blaðsíðuna, neðstu greinina og síðan upp og niður. Láta jafnvel lesa bókina svona til að geta prófað í kerfinu.',
                        'Nasdaq-vísitalan lækkaði um 4,7% í gær og Dow Jones um 3%. Lækkunin á heimsvísu hófst þegar '
                        'markaðir voru opnaðir í Asíu, þar sem helstu hlutabréfavísitölur lækkuðu um rúmlega 3%.',
                        'Við þurfum að setja upp miðlara á hljodstafir.is',
                        'Server sem keyrir nýjasta LTS version af Ubuntu Server (20.04.3 LTS)'
            ]
        return test_map

