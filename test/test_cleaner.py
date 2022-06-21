import unittest
import os
from src.manager.textprocessing_manager import Manager
import src.manager.tokens_manager as tokens


class TestCleaner(unittest.TestCase):

    def test_clean(self):
        manager = Manager()
        input_text = 'Alltaf að hreinsä allt 🥵'
        result = manager.clean(input_text)
        result_str = tokens.extract_clean(result)
        self.assertEqual('Alltaf að hreinse allt .', result_str)
        input_text = 'Leikurinn fór ca. 5-2'
        result = manager.clean(input_text)
        result_str = tokens.extract_clean(result)
        self.assertEqual('Leikurinn fór ca. 5-2', result_str)
        input_text = '§ Því fleiri, því betri'
        result = manager.clean(input_text)
        result_str = tokens.extract_clean(result)
        self.assertEqual('Því fleiri, því betri', result_str)

    def test_ssml(self):
        manager = Manager()
        input_text = 'Þetta (e. is English)'
        result = manager.clean(input_text)
        result_str = tokens.extract_clean(result, ignore_tags=False)
        self.assertEqual('Þetta <lang xml:lang="en-GB"> is English </lang>', result_str)

    def test_html_clean(self):
        manager = Manager()
        input_text = self.get_html_string()
        result = manager.clean(input_text, html=True)
        self.assertEqual(len(result), 91)
        self.assertEqual(result[0].clean, 'Í')
        self.assertEqual(result[30].ssml_start, True)
        self.assertEqual(result[31].clean, 'salutogenesis')
        self.assertEqual(result[75].ssml_end, True)
        print(tokens.extract_clean(result, ignore_tags=False))

    def test_html_table_clean(self):
        manager = Manager()
        input_text = self.get_html_string2()
        result = manager.clean(input_text, html=True)
        self.assertEqual(len(result), 401)
        self.assertEqual(result[400].clean, 'samhengi.')

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
    def get_html_string2(self):
        return '<table>   <caption id=\"hix01311\"><strong><span id=\"ilgs_2977\" class=\"sentence\">TAFLA 8</span></strong><span id=\"ilgs_2978\" class=\"sentence\"> Sex stig lífsferlis fjölskyldu </span></caption>   <tbody>     <tr>    <th id=\"hix01312\" rowspan=\"1\" colspan=\"1\"><span id=\"ilgs_2979\" class=\"sentence\">Stig </span></th>    <th id=\"hix01313\" rowspan=\"1\" colspan=\"1\"><span id=\"ilgs_2980\" class=\"sentence\">Verkefni: </span><span id=\"ilgs_2981\" class=\"sentence\">Tilfinningalegt ferli breytinga </span></th>    <th id=\"hix01314\" rowspan=\"1\" colspan=\"1\"><span id=\"ilgs_2982\" class=\"sentence\">Verkefni: </span><span id=\"ilgs_2983\" class=\"sentence\">Annars stigs breytingar sem eru nauðsynlegar þroskaferii fjölskyldunnar </span></th>     </tr>     <tr>    <td id=\"hix01315\" rowspan=\"1\" colspan=\"1\"><strong><span id=\"ilgs_2984\" class=\"sentence\">1.</span></strong><span id=\"ilgs_2985\" class=\"sentence\"> Að fara að heiman Sjálfstæðir, ungir, uppkomnir einstaklingar </span></td>    <td id=\"hix01316\" rowspan=\"1\" colspan=\"1\"><span id=\"ilgs_2986\" class=\"sentence\">Að taka tilfinningalega og fjárhagslega ábyrgð á sjálfum sér </span></td>    <td rowspan=\"1\" colspan=\"1\">      <ul>     <li id=\"hix01317\"><span id=\"ilgs_2987\" class=\"sentence\">Greina sig frá upprunafjölskyldu </span></li>     <li id=\"hix01318\"><span id=\"ilgs_2988\" class=\"sentence\">Þróa náið jafningjasamband </span></li>     <li id=\"hix01319\"><span id=\"ilgs_2989\" class=\"sentence\">Sanna sig í tengslum við starf og fjárhagslegt sjálfstæði </span></li>      </ul>    </td>     </tr>     <tr>    <td id=\"hix01320\" rowspan=\"1\" colspan=\"1\"><strong><span id=\"ilgs_2990\" class=\"sentence\">2.</span></strong><span id=\"ilgs_2991\" class=\"sentence\"> Að sameinast fjölskyldum gegnum hjónaband Ungu hjónin </span></td>    <td id=\"hix01321\" rowspan=\"1\" colspan=\"1\"><span id=\"ilgs_2992\" class=\"sentence\">Að ganga inn í nýtt kerfi </span></td>    <td rowspan=\"1\" colspan=\"1\">      <ul>     <li id=\"hix01322\"><span id=\"ilgs_2993\" class=\"sentence\">Að mynda hjúskaparkerfi </span></li>     <li id=\"hix01323\"><span id=\"ilgs_2994\" class=\"sentence\">Að aðlaga sambönd í fjölskyldunni og vinahópi að stækkun fjölskyldunnar þegar maki bætist í hópinn </span></li>      </ul>    </td>     </tr>     <tr>    <td id=\"hix01324\" rowspan=\"1\" colspan=\"1\"><strong><span id=\"ilgs_2995\" class=\"sentence\">3.</span></strong><span id=\"ilgs_2996\" class=\"sentence\"> Fjölskyldur með ung börn </span></td>    <td id=\"hix01325\" rowspan=\"1\" colspan=\"1\"><span id=\"ilgs_2997\" class=\"sentence\">Að sætta sig við nýja einstaklinga í kerfinu og í heimilishaldi </span></td>    <td rowspan=\"1\" colspan=\"1\">      <ul>     <li id=\"hix01326\"><span id=\"ilgs_2998\" class=\"sentence\">Að gera ráð fyrir barni/börnum í hjónabandinu </span></li>     <li id=\"hix01327\"><span id=\"ilgs_2999\" class=\"sentence\">Að taka þátt í barnauppeldi, fjármálum heimilisins </span></li>     <li id=\"hix01328\"><span id=\"ilgs_3000\" class=\"sentence\">Að aðlaga sambönd að stækkun fjölskyldunnar m.t.t. </span><span id=\"ilgs_3001\" class=\"sentence\">hlutverka foreldra og ömmu og afa </span></li>      </ul>    </td>     </tr>     <tr>    <td id=\"hix01329\" rowspan=\"1\" colspan=\"1\"><strong><span id=\"ilgs_3002\" class=\"sentence\">4.</span></strong><span id=\"ilgs_3003\" class=\"sentence\"> Fjölskyldur með unglinga </span></td>    <td rowspan=\"1\" colspan=\"1\">      <p id=\"hix01330\"><span id=\"ilgs_3004\" class=\"sentence\">Að auka sveigjanleika fjölskyldumarka </span></p>      <p id=\"hix01331\"><span id=\"ilgs_3005\" class=\"sentence\">Að gera ráð fyrir sjálfstæði barna og veikleikum eldri kynslóðarinnar </span></p>    </td>    <td rowspan=\"1\" colspan=\"1\">      <ul>     <li id=\"hix01332\"><span id=\"ilgs_3006\" class=\"sentence\">Að breyta sambandi foreldris og barns og leyfa unglingi að hreyfa sig inn og út úr kerfinu </span></li>     <li id=\"hix01333\"><span id=\"ilgs_3007\" class=\"sentence\">Að einbeita sér að málefnum er varða hjónaband og starfsferil á miðjum aldri </span></li>     <li id=\"hix01334\"><span id=\"ilgs_3008\" class=\"sentence\">Að hefja breytingar til þess að annast eldri kynslóðina í sameiningu </span></li>      </ul>    </td>     </tr>     <tr>    <td id=\"hix01335\" rowspan=\"1\" colspan=\"1\"><strong><span id=\"ilgs_3009\" class=\"sentence\">5.</span></strong><span id=\"ilgs_3010\" class=\"sentence\"> Börn fara að heiman og lifa sínu lífi </span></td>    <td id=\"hix01336\" rowspan=\"1\" colspan=\"1\"><span id=\"ilgs_3011\" class=\"sentence\">Að sætta sig við fjölmargar útgöngu- og inngönguleiðir í fjölskyldukerfið </span></td>    <td rowspan=\"1\" colspan=\"1\">      <ul>     <li id=\"hix01337\"><span id=\"ilgs_3012\" class=\"sentence\">Að mynda hjónabandskerfi sem tvennd á ný </span></li>     <li id=\"hix01338\"><span id=\"ilgs_3013\" class=\"sentence\">Að þróa samband milli foreldra og fullorðinna barna þeirra </span></li>     <li id=\"hix01339\"><span id=\"ilgs_3014\" class=\"sentence\">Aðlaga sambönd að því að tengdafólk og barnabörn hafa bæst í hópinn </span></li>     <li id=\"hix01340\"><span id=\"ilgs_3015\" class=\"sentence\">Að glíma við hrörnun og dauða foreldra (það er afa og ömmu) </span></li>      </ul>    </td>     </tr>     <tr>    <td id=\"hix01341\" rowspan=\"1\" colspan=\"1\"><strong><span id=\"ilgs_3016\" class=\"sentence\">6.</span></strong><span id=\"ilgs_3017\" class=\"sentence\"> Fjölskyldur á síðari hluta ævinnar </span></td>    <td id=\"hix01342\" rowspan=\"1\" colspan=\"1\"><span id=\"ilgs_3018\" class=\"sentence\">Að sætta sig við breytt hlutverk kynslóðanna </span></td>    <td rowspan=\"1\" colspan=\"1\">      <ul>     <li id=\"hix01343\"><span id=\"ilgs_3019\" class=\"sentence\">Að viðhalda virkni og áhugamálum, sem einstaklingur og sem par, þrátt fyrir líkamlega afturför; könnun á nýjum fjölskyldutengslum og félagslegum hlutverkum </span></li>     <li id=\"hix01344\"><span id=\"ilgs_3020\" class=\"sentence\">Að styðja miðkynslóðina í að gegna mikilvægu hlutverki </span></li>     <li id=\"hix01345\"><span id=\"ilgs_3021\" class=\"sentence\">Að rýma til í kerfinu fyrir visku og reynslu þeirra sem eldri eru, að styðja eldri kynslóðina án þess að yfirtaka hlutverk hennar </span></li>     <li id=\"hix01346\"><span id=\"ilgs_3022\" class=\"sentence\">Að glíma við missi maka, systkina og annarra jafningja og að undirbúa eigin dauða; æviferillinn settur í heildrænt samhengi </span></li>      </ul>    </td>     </tr>   </tbody>    </table>'

    def get_html_table(self):
        return '<table> ' \
      '<caption id="hix01290"><strong><span id="ilgs_2952" class="sentence">TAFLA 7</span></strong><span id="ilgs_2953" class="sentence"> Hlutverk sem verða til í lokuðum fjölskyldum </span></caption> ' \
      '<tbody>' \
        '<tr>' \
          '<td id="hix01291" rowspan="1" colspan="1"><strong><span id="ilgs_2954" class="sentence">Dæmi um hlutverk sem verða til í lokuðum fjölskyldum</span></strong></td>' \
        '</tr>' \
        '<tr>' \
          '<td rowspan="1" colspan="1">' \
            '<p id="hix01292"><strong><span id="ilgs_2955" class="sentence">Svarti sauðurinn</span></strong></p>' \
            '<p id="hix01293"><span id="ilgs_2956" class="sentence">Sá sem tjáir reiðina, lætur allt flakka innan fjölskyldunnar. </span></p>' \
            '<p id="hix01294"><span id="ilgs_2957" class="sentence">Er sorgmæddur innra með sér, en sorgin vekur skömm og því bregst hann við með reiði. </span></p>' \
            '<p id="hix01295"><span id="ilgs_2958" class="sentence">Kemst jafnvel í kast við lögin. </span></p>' \
          '</td>' \
        '</tr>' \
        '<tr>' \
          '<td rowspan="1" colspan="1">' \
               '<p id="hix01296"><strong><span id="ilgs_2959" class="sentence">Hetjan</span></strong></p> ' \
            '<p id="hix01297"><span id="ilgs_2960" class="sentence">Sá sem stendur sig vel og nýtur sjálfsvirðingar. </span></p> ' \
            '<p id="hix01298"><span id="ilgs_2961" class="sentence">Er háð því að vera best, ef það tekst ekki finnur hún fyrir lágu sjálfsmati. </span></p> ' \
          '</td>' \
        '</tr>' \
        '<tr>' \
          '<td rowspan="1" colspan="1">' \
            '<p id="hix01299"><strong><span id="ilgs_2962" class="sentence">Trúðurinn</span></strong></p>' \
            '<p id="hix01300"><span id="ilgs_2963" class="sentence">Sá sem tekur að sér að losa um spennu og rafmagnað andrúmsloft sem myndast þegar ekki er sagt það sem þarf að segja eða þegar tilfinningar eru ekki tjáðar. </span></p>' \
            '<p id="hix01301"><span id="ilgs_2964" class="sentence">Hann er oftast kátur og tilbúinn með skondin svör. </span></p>' \
            '<p id="hix01302"><span id="ilgs_2965" class="sentence">Er sorgmæddur innra með sér og finnur sorginni ekki farveg. </span></p>' \
          '</td>' \
        '</tr>' \
        '<tr>' \
          '<td rowspan="1" colspan="1">' \
            '<p id="hix01303"><strong><span id="ilgs_2966" class="sentence">Týndi einstaklingurinn</span></strong></p>' \
            '<p id="hix01304"><span id="ilgs_2967" class="sentence">Sá sem er oftast hljóður og tekst á við tilfinningarnar með því að hverfa inn í þögnina. </span></p>' \
            '<p id="hix01305"><span id="ilgs_2968" class="sentence">Hegðun eða andlitstjáning birtir ekki líðanina sem er mjög óræð. </span></p>' \
            '<p id="hix01306"><span id="ilgs_2969" class="sentence">Hann springur stundum og þá opnast fyrir stjórnlausa reiði. </span></p>' \
          '</td>' \
        '</tr>' \
      '</tbody>' \
    '</table>'