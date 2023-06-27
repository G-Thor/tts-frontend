from . import number_patterns as npa
from . import tuple_rules as tp

# From number_patterns, zeropnt_ptrn:
# digits in decimal numbers preceding the decimal place, can be any positive number and 0
# for example {0,}35 or {13.234,}2342
# zeropnt_ptrn = r"^(([1-9]((\d{0,2}(\.\d{3})*\.)\d{3}))|\d+|0),"


decimal_thousands_tuples = [
((npa.zeropnt_ptrn + r"\d{9}0\d*$"), '.*', 'point10', ' núll'),
((npa.zeropnt_ptrn + r"\d{8}0\d*$"), '.*', 'point9', ' núll'),
((npa.zeropnt_ptrn + r"\d{7}0\d*$"), '.*', 'point8', ' núll'),
((npa.zeropnt_ptrn + r"\d{6}0\d*$"), '.*', 'point7', ' núll'),
((npa.zeropnt_ptrn + r"\d{5}0\d*$"), '.*', 'point6', ' núll'),
((npa.zeropnt_ptrn + r"\d{4}0\d*$"), '.*', 'point5', ' núll'),
((npa.zeropnt_ptrn + r"\d{3}0\d*$"), '.*', 'point4', ' núll'),
((npa.zeropnt_ptrn + r"\d{2}0\d*$"), '.*', 'point3', ' núll'),
((npa.zeropnt_ptrn + r"\d0\d*$"), '.*', 'point2', ' núll'),
((npa.zeropnt_ptrn + r"0\d*$"), '.*', 'points', ' komma núll'),
(r"^0,\d+$", '.*', 'ones', ' núll')]


for rule, string, number in tp.ones_zip:
    decimal_thousands_tuples.append(((npa.zeropnt_ptrn + number + r"\d*$"), rule, 'points', ' komma' + string))
    decimal_thousands_tuples.append(((npa.zeropnt_ptrn + r"\d" + number + r"\d*$"), rule, 'point2', string))
    decimal_thousands_tuples.append(((npa.zeropnt_ptrn + r"\d{2}" + number + r"\d*$"), rule, 'point3', string))
    decimal_thousands_tuples.append(((npa.zeropnt_ptrn + r"\d{3}" + number + r"\d*$"), rule, 'point4', string))
    decimal_thousands_tuples.append(((npa.zeropnt_ptrn + r"\d{4}" + number + r"\d*$"), rule, 'point5', string))
    decimal_thousands_tuples.append(((npa.zeropnt_ptrn + r"\d{5}" + number + r"\d*$"), rule, 'point6', string))
    decimal_thousands_tuples.append(((npa.zeropnt_ptrn + r"\d{6}" + number + r"\d*$"), rule, 'point7', string))
    decimal_thousands_tuples.append(((npa.zeropnt_ptrn + r"\d{7}" + number + r"\d*$"), rule, 'point8', string))
    decimal_thousands_tuples.append(((npa.zeropnt_ptrn + r"\d{8}" + number + r"\d*$"), rule, 'point9', string))
    decimal_thousands_tuples.append(((npa.zeropnt_ptrn + r"\d{9}" + number + r"\d*$"), rule, 'point10', string))

#for rule, string, number in tp.dec_ones_male:
#    decimal_thousands_tuples.append(((npa.ones_ptrn_no11 + number + npa.dec_ptrn_def), rule, 'ones', string))

# We pronounce the decimals of small numbers as a unit, not separate numbers:
# 5,25 -> fimm komma tuttugu og fimm - and not: fimm komma tvö fimm
decimal_small_tuples = [
((npa.zeropnt_ptrn + r"0\d*$"), '.*', 'points', ' núll'),
((npa.zeropnt_ptrn + r"\d+$"), '.*', 'point_only', ' komma'),
(r"^0,\d+$", '.*', 'ones', ' núll')]

for rule, string, number in tp.ones_zip:
    decimal_small_tuples.append(((npa.zeropnt_ptrn + r"\d" + number + r"\d*$"), rule, 'points_ones', string))
    decimal_small_tuples.append(((npa.zeropnt_ptrn + number + r"$"), rule, 'points_ones', string))

for string, number in tp.tens_zip:
    decimal_small_tuples.append(((npa.zeropnt_ptrn + number + r"\d*$"), '.*', 'points_tens', string))

for string, number in tp.dozens_zip:
    decimal_small_tuples.append(((npa.zeropnt_ptrn + number + r"0$"), '.*', 'points_dozens', string))
    decimal_small_tuples.append(((npa.zeropnt_ptrn + number + r"[1-9]$"), '.*', 'points_dozens', string + ' og'))
