import re
import difflib
from typing import Tuple

from . import abbr_dict as abd 
from . import area_dict as ad
from . import currency_dict as cd
from . import denominator_dict as dend
from . import direction_dict as dird
from . import distance_dict as dd
from . import electronic_dict as ed
from . import period_dict as pd
from . import rest_dict as rd
from . import time_dict as td
from . import volume_dict as vd
from . import weight_dict as wd
from . import pre_help_dicts as phd
from . import symbols_dict as sd

direction_ptrn = r"[SN]?V|N|[SN]?A|S"

pre_help_dict = phd.pre_help_dicts
abbr_dict = abd.abbr_dict
area_dict = ad.make_area_dict()
currency_dict = cd.make_currency_dict()
denominator_dict = dend.denominator_dict
direction_dict = dird.direction_dict
distance_dict = dd.make_distance_dict()
electronic_dict = ed.make_electronic_dict()
period_dict = pd.make_period_dict()
rest_dict = rd.make_rest_measure_dict()
time_dict = td.make_time_dict()
volume_dict = vd.make_volume_dict()
weight_dict = wd.make_weight_dict()
symb_dict = sd.symb_dict


class Normalized:

    def __init__(self, original: str, ind: int, start: int, end: int):
        self.original_token = original
        self.index = ind
        self.span_start = start
        self.span_end = end
        self.normalized = ''


def replace_in_list(token_list: list, original_list: list, token: str, replacement: str) -> list:
    """Replace all occurrences of 'token' with 'replacement' in the 'token_list'"""

    #replaced_list = [replacement if item == token else item for item in token_list]
    replaced_list = []
    zipped_list = []
    for ind, item in enumerate(token_list):
        if item == token:
            replaced_list.append(replacement)
            zipped_list.append((original_list[ind], replacement))
        else:
            replaced_list.append(item)
            zipped_list.append((original_list[ind], item))
    return replaced_list, zipped_list


def get_replacement(orig_text: str, replacement_text: str) -> Tuple[str, str]:
    """ Find the difference between the two input strings and extract the corresponding tokens.
    Return both tokens. """
    diff = difflib.ndiff(orig_text.split(' '), replacement_text.split(' '))
    to_replace = ''
    replacement = ''
    for d in diff:
        if d.startswith('-'):
            to_replace += ' ' + d.split(' ')[1]
        elif d.startswith('+'):
            replacement += ' ' + d.split(' ')[1]
    return to_replace.strip(), replacement.strip()


def replace_all_old(current_sent: list, original_list: list, dic: dict, ptrn="") -> list:
    """ Replace words according to the appropriate dictionary.
    Return a list of tuples, containing original tokens and replacements."""

    replaced_list = current_sent
    #current_text = ' '.join(current_sent)
    current_text = ''
    for tok in current_sent:
        current_text += tok.normalized_token + ' '

    zipped_result = zip(current_sent, replaced_list)
    if re.findall(ptrn, current_text):
        for i, j in dic.items():
            indices = re.finditer(i, current_text)
            if indices:
                sub_text = re.sub(i, j, current_text)
                to_replace, replacement = get_replacement(current_text, sub_text)


                #replaced_list = replace_in_list(replaced_list, to_replace, replacement)
                replaced_list, zipped_result = replace_in_list(current_text.split(), original_list, to_replace, replacement)
                current_text = sub_text
        #zipped_result = zip(original_list, replaced_list)
    result_list = list(zipped_result)
    return result_list, replaced_list

# replace words according to the appropriate dictionary
def replace_all(text, dic, ptrn=""):
    if re.findall(ptrn, text):
        for i, j in dic.items():
            text = re.sub(i, j, text)
    return text

# replace words according to the appropriate domain 
def replace_domain(splitsent, domain, ptrn=r"\-|\–|\—"):
    finalstring = ""
    replacement_index = []
    for i in range(len(splitsent)):
        try:
            # original: does not work as intended, since at i == 0 splitsent[i-1] is the last element (splitsent[-1])
            # of the array, so check for zero first
            # if re.match(r"\d", splitsent[i-1]) and re.match(ptrn, splitsent[i]) and re.match(r"\d", splitsent[i+1]):
            if i > 0 and re.match(r"\d", splitsent[i - 1]) and re.match(ptrn, splitsent[i]) and re.match(r"\d", splitsent[i + 1]):
                replacement_index.append(i)
                if domain == 'sport':
                    splitsent[i] = ""
                else:
                    splitsent[i] = "til"
            # this is a potential negative number, like '-4,5', replace '-' with 'mínus'
            elif re.match(ptrn, splitsent[i]) and re.match(r"\d", splitsent[i+1]):
                splitsent[i] = "mínus"
        except:
            pass
        finalstring += splitsent[i] + " "
    #return finalstring
    return " ".join(splitsent)
    #return replacement_index


def init_normalized(sent: str) -> list:
    norm_list = []
    sent_arr = sent.split()
    char_counter = 0
    for i, tok in enumerate(sent_arr):
        start = sent.index(tok, char_counter)
        norm_list.append(Normalized(tok, i, start, start+len(tok)))
    return norm_list


def replace_abbreviations(sent, domain):
    norm_list = init_normalized(sent)

    sent = replace_all(sent, direction_dict, direction_ptrn)
    sent = replace_all(sent, pre_help_dict)
    sent = replace_all(sent, denominator_dict, r"\/")
    sent = replace_all(sent, weight_dict, wd.weight_ptrn)
    sent = replace_all(sent, distance_dict, dd.distance_ptrn)
    sent = replace_all(sent, area_dict, ad.area_ptrn)
    sent = replace_all(sent, volume_dict, vd.volume_ptrn)
    sent = replace_all(sent, time_dict, td.time_ptrn)
    sent = replace_all(sent, currency_dict, cd.currency_ptrn)
    sent = replace_all(sent, electronic_dict, ed.electronic_ptrn)
    sent = replace_all(sent, rest_dict, rd.rest_ptrn)
    sent = replace_all(sent, period_dict, pd.period_ptrn)
    sent = replace_all(sent, abbr_dict)
    sent = replace_domain(sent.split(), domain)
    return sent

