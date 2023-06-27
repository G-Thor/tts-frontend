import re

from . import number_help as nh

from . import abbr_patterns as ap
from . import abbr_functions as af

from . import cardinal_ones_tuples as cot
from . import cardinal_thousands_tuples as ctt
from . import cardinal_million_tuples as cmt
from . import cardinal_big_tuples as cbt
from . import ordinal_ones_tuples as oot
from . import ordinal_thousands_tuples as ott
from . import ordinal_million_tuples as omt
from . import ordinal_big_tuples as obt
from . import decimal_thousands_tuples as dtt
from . import fraction_tuples as ft
from . import sport_tuples as st
from . import time_tuples as tt

from . import symbols_dict as sd

cardinal_thousand_tuples = cot.cardinal_ones_tuples + ctt.cardinal_thousands_tuples
cardinal_million_tuples = cardinal_thousand_tuples + cmt.cardinal_million_tuples
cardinal_big_tuples = cardinal_million_tuples + cbt.cardinal_big_tuples
ordinal_thousand_tuples = (
    oot.ordinal_ones_tuples
    + ctt.cardinal_thousands_tuples
    + ott.ordinal_thousands_tuples
)
ordinal_million_tuples = (
    ordinal_thousand_tuples + cmt.cardinal_million_tuples + omt.ordinal_million_tuples
)
ordinal_big_tuples = (
    ordinal_million_tuples + cbt.cardinal_big_tuples + obt.ordinal_big_tuples
)
decimal_thousand_tuples = cardinal_thousand_tuples + dtt.decimal_thousands_tuples
decimal_small_tuples = cardinal_thousand_tuples + dtt.decimal_small_tuples
decimal_big_tuples = cardinal_big_tuples + dtt.decimal_thousands_tuples
fraction_tuples = cardinal_thousand_tuples + ft.fraction_tuples
sport_tuples = st.sport_tuples
time_tuples = tt.time_tuples

symb_dict = sd.symb_dict
# Every thing that does not only contain alphabetic characters and spaces
symb_ptrn = r"[^A-ZÁÐÉÍÓÚÝÞÆÖa-záðéíóúýþæö\s]"


def make_dict(word, type_cols):
    """Create a dictionary with 'word' as key and a dictionary as value. The dictionary has each item
    from 'type_cols' as keys and each key has an empty string as value. These values will be filled
    during later processing steps, according to the number represented by 'word'.
    'type_cols' typically contains a list of positions in a number, e.g. ['thousands', 'hundreds', 'dozens', ...].
    """
    value_dict = {}
    value_dict[word] = {type_cols[0]: ""}
    for col in type_cols[1:]:
        value_dict[word].update({col: ""})
    return value_dict


# Fill the dictionaries with values from appropriate number tuples
# Example: word = 4, tuple = ("\d*4", "nvfn", "ones", "fjórar")
# The number 4 followed by a feminine, plural, nominative noun becomes fjórar
def fill_dict(word: str, pos_tag: str, tuples: list, type_dict: dict, cols: list):
    """
    Iterates over all tuples in 'tuples' and searches for a match for 'word' and 'pos_tag' in each tuple.
    On a match, sets the value of the matching positional label in 'type_dict' to the verbalization in the matching tuple.

    Example:
    a match for word='10,1' and pos_tag='nkeþ' is found in a tuple (note that pos-tag does not matter for the number ten)
    ('^((([1-9]((\\d{0,2}(\\.\\d{3})*\\.)|\\d*))\\d)|[1-9])?10((,\\d*)|(\\s1\\/2|\\s?(½|⅓|¼|⅔|¾)))?$', '.*', 'dozens', 'tíu'
    the value for 'dozens' in the 'type_dict' will then be set to 'tíu'

    :param word: the word representing the number to normalize
    :param pos_tag: the part-of-speech tag of the next token
    :param tuples: a (potentially very large) list of 4-tuples of the form: (digit_regex, pos_tag_regex, positional_label, verbalization)
    :param type_dict: a dictionary as created in make_dict()
    :param cols: a list of positional labels, the keys from the value dictionary in type_dict
    :return: a string composed of all set values in type_dict
    """
    verbalization = ""
    for i in range(len(tuples)):
        if re.findall(tuples[i][0], word) and re.findall(tuples[i][1], pos_tag):
            try:
                type_dict[word][tuples[i][2]] = tuples[i][3]
                print(type_dict[word][tuples][i][4])
                tuples[i][4] = 18
                print(tuples[i])
            except:
                pass
    for col in cols:
        verbalization += type_dict[word][col]
    return verbalization


def digit_fun(digit_str: str) -> str:
    """
    Resolve each single digit and symbol character by character, similar to
    SSML <say-as interpret-as="characters">.
    The following symbols are also resolved to a word representation (except '-' which is replaced by <sil>):
    - + . : , / -> <sil>, plús, punktur, tvípunktur, komma, skástrik
    See: number_help.digit_numbers

    :param digit_str: a string containing digits and possibly selected symbols
    :return: a string where digits and symbols have been replaced with their word representation
    """
    digit_str = re.sub(" ", "<sil> ", digit_str)
    for digit, word in nh.digit_numbers:
        digit_str = re.sub(digit, word, digit_str)
    return digit_str


# Expand the ordinal digits, the expansion of digits_ord is in number_help
def digit_ord_fun(substr):
    for digit, word in nh.digits_ord:
        substr = re.sub(r"^0" + digit + r"\.$", "núll " + word, substr)
    return substr


def wlink_fun(text, ptrn=ap.link_ptrn_all):
    if re.findall(ptrn, text):
        substr = " ".join(text)
        for symbol, word in nh.wlink_numbers:
            substr = re.sub(symbol, word, substr)
        print(substr)
        return substr


# Fill in the number appropriately based on pattern
def number_findall(word, tag, domain):
    normalized_str = ""
    if re.findall(nh.ordinal_thousand_ptrn, word):
        ordinal_thousand_dict = make_dict(word, nh.int_cols_thousand)
        tmpword = fill_dict(
            word,
            tag,
            ordinal_thousand_tuples,
            ordinal_thousand_dict,
            nh.int_cols_thousand,
        )

    elif re.findall(nh.ordinal_million_ptrn, word):
        ordinal_million_dict = make_dict(word, nh.int_cols_million)
        tmpword = fill_dict(
            word, tag, ordinal_million_tuples, ordinal_million_dict, nh.int_cols_million
        )

    elif re.findall(nh.ordinal_big_ptrn, word):
        ordinal_big_dict = make_dict(word, nh.int_cols_big)
        tmpword = fill_dict(
            word, tag, ordinal_big_tuples, ordinal_big_dict, nh.int_cols_big
        )

    elif re.findall(nh.cardinal_thousand_ptrn, word):
        cardinal_thousand_dict = make_dict(word, nh.int_cols_thousand)
        tmpword = fill_dict(
            word,
            tag,
            cardinal_thousand_tuples,
            cardinal_thousand_dict,
            nh.int_cols_thousand,
        )

    elif re.findall(nh.cardinal_million_ptrn, word):
        cardinal_million_dict = make_dict(word, nh.int_cols_million)
        tmpword = fill_dict(
            word,
            tag,
            cardinal_million_tuples,
            cardinal_million_dict,
            nh.int_cols_million,
        )

    elif re.findall(nh.cardinal_big_ptrn, word):
        cardinal_big_dict = make_dict(word, nh.int_cols_big)
        tmpword = fill_dict(
            word, tag, cardinal_big_tuples, cardinal_big_dict, nh.int_cols_big
        )

    # changed by ABN: check specially for a small decimal pattern to pronounce as a unit and not as
    # separate numbers. If that (original) behaviour is wanted, skip this test and go straight to the next
    # 'elif'-clause.
    elif re.findall(nh.decimal_small_ptrn, word):
        decimal_thousand_dict = make_dict(word, nh.decimal_cols_small)
        tmpword = fill_dict(
            word,
            tag,
            decimal_small_tuples,
            decimal_thousand_dict,
            nh.decimal_cols_small,
        )

    elif re.findall(nh.decimal_thousand_ptrn, word):
        decimal_thousand_dict = make_dict(word, nh.decimal_cols_thousand)
        tmpword = fill_dict(
            word,
            tag,
            decimal_thousand_tuples,
            decimal_thousand_dict,
            nh.decimal_cols_thousand,
        )

    elif re.findall(nh.decimal_big_ptrn, word):
        decimal_big_dict = make_dict(word, nh.decimal_cols_big)
        tmpword = fill_dict(
            word, tag, decimal_big_tuples, decimal_big_dict, nh.decimal_cols_big
        )

    elif re.findall(nh.time_ptrn, word):
        time_dict = make_dict(word, nh.time_sport_cols)
        tmpword = fill_dict(word, tag, time_tuples, time_dict, nh.time_sport_cols)

    elif re.findall(nh.fraction_ptrn, word):
        if domain == "other" or re.findall("½|⅓|⅔|¼|¾", word):
            fraction_dict = make_dict(word, nh.decimal_cols_thousand)
            tmpword = fill_dict(
                word, tag, fraction_tuples, fraction_dict, nh.decimal_cols_thousand
            )
        elif domain == "sport":
            sport_dict = make_dict(word, nh.time_sport_cols)
            tmpword = fill_dict(word, tag, sport_tuples, sport_dict, nh.time_sport_cols)

    elif re.findall(r"^0\d\.$", word):
        tmpword = digit_ord_fun(word)
    else:
        tmpword = digit_fun(word)
    word = tmpword
    return word


# Fill in the number, letter, link or symbol based on the tag of the next word
def handle_sentence(sent, domain, tagger):
    returnsent = ""
    sentsplit = sent.split()
    tagsent = tagger.tag_sent(sentsplit)
    split_zip = list(zip(sentsplit, list(tagsent[1:]) + [""]))
    res_tuples = []
    tag_counter = 0
    print(" ".join(sentsplit))
    for word, nexttag in split_zip:
        orig_word = word
        if re.match(r"[\d½⅓¼⅔¾\-\–]", word):
            word = number_findall(word, nexttag, domain)
        if re.match(nh.roman_letters_ptrn, word):
            word = " ".join(word)
        elif re.match(nh.letters_ptrn, word):
            word = " ".join(word)
        elif re.match(ap.link_ptrn_all, word):
            word = wlink_fun(word)
        elif re.match(symb_ptrn, word):
            word = af.replace_all(word, symb_dict, symb_ptrn)
        returnsent += word + " "
        res_tuples.append((orig_word, word, tagsent[tag_counter]))
        tag_counter += 1
    # return returnsent
    return res_tuples
