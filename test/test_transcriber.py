import unittest
import os
from src.manager.textprocessing_manager import Manager
import src.manager.tokens_manager as tokens


class TestTranscriber(unittest.TestCase):

    def test_simple_transcript(self):
        manager = Manager()
        input_text = 'hlaupa'
        transcribed = manager.transcribe(input_text)
        result_str = tokens.extract_transcribed_text(transcribed)
        self.assertEqual('l_0 9i: p a', result_str)

    def test_single_letters(self):
        manager = Manager()
        input_text = 'nýjasta LTS version af Ubuntu Server (20.04.3 LTS)'
        transcribed = manager.transcribe(input_text)
        result_str = tokens.extract_transcribed_text(transcribed)
        self.assertEqual('n i: j a s t a E t l_0 t_h j E: E s v 9 r s j O n a: f Y n_0 t Y s 9: r v E '
 'r t_h v ei: r n u l p_h u n_0 t Y r n u l f j ou: r I r p_h u n_0 t Y r T r '
 'i: r E t l_0 t_h j E: E s', result_str)

    def test_word_sep_transcribe(self):
        manager = Manager()
        manager.set_g2p_word_separator('-')
        test_string = 'hlaupa í burtu í dag'
        transcribed = manager.transcribe(test_string)
        result_str = tokens.extract_transcribed_text(transcribed, word_separator='-')
        self.assertEqual('l_0 9i: p a - i: - p Y r_0 t Y - i: - t a: G', result_str)

    def test_syllabification(self):
        manager = Manager()
        manager.set_g2p_syllab_symbol('.')
        test_string = 'hlaupa í burtu í dag'
        transcribed = manager.transcribe(test_string)
        result_str = tokens.extract_transcribed_text(transcribed)
        self.assertEqual('l_0 9i: . p a i: p Y r_0 . t Y i: t a: G', result_str)

    def test_custom_dict(self):
        manager = Manager()
        custom_dict = self.get_custom_dict()
        manager.set_g2p_custom_dict(custom_dict)
        test_string = 'þessi texti en engir aukvisar'
        transcribed = manager.transcribe(test_string)
        result_str = tokens.extract_transcribed_text(transcribed)
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

    def test_longer_text_3(self):
        manager = Manager()
        test_string = self.get_parsed_html()
        transcribed = manager.transcribe(test_string, phrasing=True)
        result_arr = manager.get_sentence_representation(transcribed, ignore_tags=False)
        #for sent in result_arr:
        #    print(sent)
        self.assertEqual(len(result_arr), 3)
        self.assertEqual(result_arr[2],
                         'a n_0 t O n O v s c i s i n t I f r a m au: <sil> a: D <sil> E: f ei n s t a h k l i N k a r s E: m Y h p l I v D Y au: l a G s '
                         'ai j Y t_h I l k au N k m E: D r ei n s t l Y s I n I <sil> T au: T r ou: a D I s t m E: D T ei: m t_h I l f I n i N k f I: r I r '
                         's a m h ei J c I i: l i: v I n Y <sil> E n s k a <sil> s E n s O: v k_h ou: E r E N_0 k <sil> s I G r u n k Y n a r_0 s t ou h t I r '
                         'h E: v Y r i s t l E n s k a D s c I l k r ei n i N k Y h Y G t_h a k s I n s Y m t_h I l f I n i N k Y f I: r I r '
                         's a m h ei J c I i: l i: v I n Y au: E f t I r_0 f a r a n t I h au h t <sil>')

    def test_longer_text_4(self):
        manager = Manager()
        test_string = self.get_problematic_html()
        transcribed = manager.transcribe(test_string, phrasing=True, html=True)
        result_arr = manager.get_sentence_representation(transcribed, ignore_tags=False)
        #for sent in result_arr:
        #    print(sent)
        self.assertEqual(len(result_arr), 17)

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

    def get_parsed_html(self):
        return 'Í kjölfarið sýndi hann fram á að það stuðli að heilbrigði ef einstaklingar geti fundið samhengi í ' \
               'tengslum við lífsatburði eða öðlast skilning á aðstæðum sínum. Hann taldi uppsprettu ' \
               'heilbrigðis <lang xml:lang="en-GB"> salutogenesis </lang> vera að finna í mismunandi hæfni einstaklinga ' \
               'til að stjórna viðbrögðum sínum við álagi. Antonovsky sýndi fram á að ef einstaklingar sem upplifðu ' \
               'álag sæju tilgang með reynslu sinni, þá þróaðist með þeim tilfinning fyrir samhengi í ' \
               'lífinu <lang xml:lang="en-GB"> sense of coherence </lang> Sigrún Gunnarsdóttir hefur íslenskað ' \
               'skilgreiningu hugtaksins um tilfinningu fyrir samhengi í lífinu á eftirfarandi hátt: '

    def get_parsed_html_tmp(self):
        return 'heilbrigðis <lang xml:lang="en-GB"> salutogenesis </lang> vera að finna í mismunandi hæfni einstaklinga ' \
               'lífinu <lang xml:lang="en-GB"> sense of coherence </lang> Sigrún Gunnarsdóttir hefur íslenskað '

    def get_problematic_html(self):
        return '<!DOCTYPE html><html>     <head>         <title>Prufuskjal fyrir talgervil</title>     </head>     ' \
               '<body>         <h1> Hljóðstafir - Stutt verkefnislýsing</h1>         <p>Tilgangur verkefnisins:</p>         ' \
               '<p>1. Er að auðvelda framleiðslu aðgengilegra bóka með texta og fjölga þeim til muna í safni HBS.</p>         ' \
               '<p>2. Veita útgefendum aðgang að kerfi þar sem þeir geta tekið texta og hljóð sem eru formuð eftir ' \
               'skilgreiningu HBS (sem byggir á alþjóðastöðlum) og sett saman sem aðgengilega bók með texta</p>         ' \
               '<p>Forsendur:</p>         <p>· Tækniumhverfi sem virkar til að gera sem flestar bækur eins ' \
               'sjálfvirkt og völ er á</p>         <p>o Í dag erum við að nota aeneas/ascanias sem virka ágætlega ' \
               'fyrir einfaldar bækur.</p>         <p>· Tími fyrir starfsfólk til að vinna einfaldari bækur, mestur ' \
               'tími Alfreðs fer í flóknari bækur</p>         <p>o Erfiðar námsbækur hafa verið í mestum forgangi</p>         ' \
               '<p>o Hugleiða að ráða tímabundið starfsmann í þessa vinnu</p>         <p>· Við þurfum að hafa ' \
               'texta og hljóð af sömu bókum sem hægt er að nota til að búa til aðgengilegar bækur</p>         ' \
               '<p>o Hversu margar bækur þarf?</p>         <p>§ Því fleiri, því betri</p>         <p>§ Þurfa að ' \
               'vera öðruvísi, hvort sem er tungumál, hraði á lestri, gæði á hljóðfælum, allskonar edge-case, ' \
               'til að ná að tvíka og laga og gera sjálfvirkt.</p>         <p>§ Gætum byrjað á Harry Potter</p>        ' \
               ' <p>o Öll flækjustig bóka í upphafi eða byrja á einfaldari bókum?</p>         <p>§ Frá léttustu bókum ' \
               'upp í erfiðustu bækurnar</p>         <p>· Kennslubækur með myndir, lestur ekki 100% línulaga, ' \
               'horizontal lesið, upp og niður allsstaðar í gegnum blaðsíðuna, neðstu greinina og síðan upp og niður. ' \
               'Láta jafnvel lesa bókina svona til að geta prófað í kerfinu.</p>         <p>o Þetta síðasta, ef tækist ' \
               'að leysa, myndi leysa mjög mörg edge-case, forritunaraðferð.</p>         <p>· Prófa ' \
               'líka aðkeyptar bækur</p>         <p>·</p>         <p>· Við þurfum að setja upp miðlara á ' \
               'hljodstafir.is</p>         <p>o Server sem keyrir nýjasta LTS version af Ubuntu Server ' \
               '(20.04.3 LTS) </p>     </body> </html>'
