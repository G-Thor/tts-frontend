
from cleaner_manager import clean_text, clean_html_text
from normalizer_manager import normalize_token_list


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

def main():
    input_text = "Leikurinn fór, ca. 5-2 í gær."
    #input_text = get_html_text()
    clean = clean_text(input_text)
    print("============== CLEAN TOKENS =======================")
    print(clean)
    normalized = normalize_token_list(clean)
    print("============== NORMALIZED TOKENS ==================")
    print(normalized)

if __name__ == '__main__':
    main()