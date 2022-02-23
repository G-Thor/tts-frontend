"""
Handles the communication with the phrasing module. The result of the phrasing methods in phrasing_manager is
a list of NormalizedTokens, the same as the input from the normalizer_manager. The phrasing module adds TagTokens
where it assumes a good place for a speech pause.
"""
import os

from typing import Union
from tokens import Token, CleanToken, NormalizedToken, TagToken
from tokens_manager import extract_tagged_text
from Phrasing.phrasing import Phrasing


def parse_text(tagged_text: str):
    MANAGER_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT, tail = os.path.split(MANAGER_PROJECT_ROOT)
    os.chdir(PROJECT_ROOT + '/phrasing-tool/Phrasing/IceNLP/bat/iceparser')
    with open('tagged_tmp.txt', 'w') as f:
        f.write(tagged_text)
    comm = './iceparser.sh -i tagged_tmp.txt -o ../../../parsed_tmp.txt'
    os.system(comm)
    os.remove('tagged_tmp.txt')
    os.chdir(PROJECT_ROOT)

    with open('phrasing-tool/Phrasing/parsed_tmp.txt') as file:
        lines = [line.strip() for line in file]
    phraser = Phrasing()
    paused_text = phraser.insert_pauses(lines)
    os.remove('phrasing-tool/Phrasing/parsed_tmp.txt')
    return paused_text


def phrase_token_list(normalized_tokens: list) -> list:
    """Send the pos-tagged text in normalized tokens through
    the phrasing module and returns the list with inserted TagTokens where appropriate."""
    tagged_text = extract_tagged_text(normalized_tokens)
    parsed = parse_text(tagged_text)
    return parsed
