import pycountry

from tokens_manager import extract_text
from cleaner_manager import clean_text, clean_html_text
from normalizer_manager import normalize_token_list
from phrasing_manager import phrase_token_list
from g2p_manager import transcribe


def get_html_table():
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

def get_html_text():
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

def get_normalized_law_text():
    return 'Áttu ákvæði  önnur málsgrein  fimmta grein laga númer hundrað þrjátíu og átta /  tvö þúsund og þrjú því ' \
           'heldur ekki við umrætt tímabil , þar sem á því tímabili var hvorki framlengdur eldri samningur né gerður nýr ' \
           'tímabundinn samningur innan sex vikna frá lokum eldri samnings . '


def main():
    input_text = get_html_table()
    clean = clean_html_text(input_text)
    print("============== CLEAN TOKENS =======================")
    print(clean)
    print(extract_text(clean))
    normalized = normalize_token_list(clean)
    print("============== NORMALIZED TOKENS ==================")
    print(normalized)
    phrased = phrase_token_list(normalized)
    for token in phrased:
        print(token)
    transcribed = transcribe(phrased)
    for token in transcribed:
        print(token)
    print(extract_text(transcribed, False))


if __name__ == '__main__':
    main()