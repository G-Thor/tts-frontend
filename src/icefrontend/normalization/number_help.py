int_cols_thousand = ["thousands", "hundreds", "dozens", "ones"]

int_cols_million = [
    "hundred thousands",
    "ten thousands",
    "thousands",
    "hundreds",
    "dozens",
    "ones",
]

int_cols_big = [
    "hundred billions",
    "ten billions",
    "billions",
    "hundred millions",
    "ten millions",
    "millions",
    "hundred thousands",
    "ten thousands",
    "thousands",
    "hundreds",
    "dozens",
    "ones",
]

decimal_cols_small = [
    "hundreds",
    "dozens",
    "ones",
    "point_only",
    "points",
    "points_tens",
    "points_dozens",
    "points_ones",
]

decimal_cols_thousand = [
    "thousands",
    "hundreds",
    "dozens",
    "ones",
    "points",
    "point2",
    "point3",
    "point4",
    "point5",
    "point6",
    "point7",
    "point8",
    "point9",
    "point10",
]

decimal_cols_big = [
    "hundred billions",
    "ten billions",
    "billions",
    "hundred millions",
    "ten millions",
    "millions",
    "hundred thousands",
    "ten thousands",
    "thousands",
    "hundreds",
    "dozens",
    "ones",
    "points",
    "point2",
    "point3",
    "point4",
    "point5",
    "point6",
    "point7",
    "point8",
    "point9",
    "point10",
]


# time, timedigit, sport
time_sport_cols = [
    "first_ten",
    "first_one",
    "between_teams",
    "second_ten",
    "second_one",
]

ordinal_thousand_ptrn = r"^([1-9]\.?\d{3}|[1-9]\d{0,2}|0)\.$"
ordinal_million_ptrn = r"^[1-9]\d{0,2}\.?\d{3}\.$"
ordinal_big_ptrn = r"^[1-9]\d{0,2}(\.\d{3}){2,3}\.$"

cardinal_thousand_ptrn = r"^([1-9]\.?\d{3}|[1-9]\d{0,2})$"
cardinal_million_ptrn = r"^[1-9]\d{0,2}\.?\d{3}$"
cardinal_big_ptrn = r"^[1-9]\d{0,2}(\.\d{3}){2,3}$"

# small decimal numbers with max two decimal places, decimal digits should be pronounced as the whole number
# e.g. 5,14 should be 'fimm komma fjórtán' and not 'fimm komma einn fjórir'
decimal_small_ptrn = r"^([1-9]\d{0,3}|0),\d{1,2}$"
# for larger decimal numbers the decimal digits are pronounced digit by digit:
# 45,4053 : fjörutíu og fimm komma fjórir núll fimm þrír
decimal_thousand_ptrn = r"^([1-9]\.?\d{3}|[1-9]\d{0,2}|0),\d+$"
decimal_big_ptrn = r"^[1-9]\d{0,2}\.?(\d{3}){1,3},\d+$"

fraction_ptrn = r"^([1-9]\d{0,2} ?)?([1-9]\d*\/([2-9]|[1-9]\d+)|(½|⅓|⅔|¼|¾))$"
time_ptrn = r"^(([01]?\d|2[0-4])[:\.][0-5]|0)\d$"
sport_ptrn = r"^(?!1\/2)([1-9]\d?\/[1-9]\d?)$"

# TODO: put the exceptions in an external file, develop heuristic as for when to spell out and when not
letters_ptrn = r"^(?!^(RÚV|SPRON|EFTA|AIDS|NATO|FIFA|UNESCO|UNICEF|WHO|ESA|APEC|OPEC\-|\.)$)[\-\.A-ZÁÐÉÍÓÚÝÞÆÖ]{1,4}$"
roman_letters_ptrn = r"[IVXLCDM]{4,20}"

symbol_ptrn = r"^[^A-ZÁÐÉÍÓÚÝÞÆÖa-záðéíóúýþæö\d]$"

digit_numbers = [
    ("0", " núll"),
    ("1", " einn"),
    ("2", " tveir"),
    ("3", " þrír"),
    ("4", " fjórir"),
    ("5", " fimm"),
    ("6", " sex"),
    ("7", " sjö"),
    ("8", " átta"),
    ("9", " níu"),
    (r"\-", " <sil>"),
    (r"\+", " plús"),
    (r"\.", " punktur"),
    (r"\*", "sinnum"),
    # TODO: is a colon ever read as 'tvípunktur' in a string of digits?
    # When representing time, it is not read. Other examples?
    # (':', ' tvípunktur'),
    (":", ""),
    (",", " komma"),
    (r"\/", " deilt með"),
]

digits_ord = [
    ("0", "núllta"),
    ("1", "fyrsta"),
    ("2", "annan"),
    ("3", "þriðja"),
    ("4", "fjórða"),
    ("5", "fimmta"),
    ("6", "sjötta"),
    ("7", "sjöunda"),
    ("8", "áttunda"),
    ("9", "níunda"),
]

wlink_numbers = [
    ("0", "núll"),
    ("1", "einn"),
    ("2", "tveir"),
    ("3", "þrír"),
    ("4", "fjórir"),
    ("5", "fimm"),
    ("6", "sex"),
    ("7", "sjö"),
    ("8", "átta"),
    ("9", "níu"),
    (r"\.", "punktur"),
    (r"\-", "bandstrik"),
    (r"\/", "deilt með"),
    ("_", "undirstrik"),
    ("@", "hjá"),
    (":", "tvípunktur"),
    ("=", "jafnt og"),
    (r"\*", "sinnum"),
    (r"\?", "spurningarmerki"),
    ("!", "upphrópunarmerki"),
    ("&", "og"),
    ("%", "prósent"),
    ("#", "myllumerki"),
]
