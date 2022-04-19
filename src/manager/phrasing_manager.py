"""
Handles the communication with the phrasing module. The result of the phrasing methods in phrasing_manager is
a list of NormalizedTokens, the same as the input from the normalizer_manager. The phrasing module adds TagTokens
where it assumes a good place for a speech pause.
"""
import os
from .tokens import NormalizedToken, TagToken
from .tokens_manager import extract_tagged_text
from phrasing.phrasing import Phrasing

# used to replace punctuation in normalized text if we don't perform real phrasing analysis
SIL_TAG = '<sil>'

class PhrasingManager:

    def is_punct(self, tok: NormalizedToken):
        return tok.pos == '.' or tok.pos == ',' or tok.pos == 'pg' or tok.pos == 'pa' or tok.name == '/'

    def phrase_text(self, tagged_text: str):
        MANAGER_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
        PROJECT_ROOT, tail = os.path.split(MANAGER_PROJECT_ROOT)
        os.chdir(PROJECT_ROOT + '/manager/IceNLP/bat/iceparser')
        print('PROJECT_ROOT: ' + PROJECT_ROOT)
        with open('tagged_tmp.txt', 'w') as f:
            f.write(tagged_text)
        comm = './iceparser.sh -i tagged_tmp.txt -o ../../../parsed_tmp.txt'
        os.system(comm)
        os.remove('tagged_tmp.txt')
        os.chdir(PROJECT_ROOT)
        with open(PROJECT_ROOT + '/manager/parsed_tmp.txt') as file:
            lines = [line.strip() for line in file]
        phraser = Phrasing()
        paused_text = phraser.insert_pauses(lines)
        os.remove(PROJECT_ROOT + '/manager/parsed_tmp.txt')

        return paused_text

    def phrase_token_list(self, normalized_tokens: list) -> list:
        """Send the pos-tagged text in normalized tokens through
        the phrasing module and returns the list with inserted TagTokens where appropriate."""
        tagged_text = extract_tagged_text(normalized_tokens)
        phrased = self.phrase_text(tagged_text)
        phrased_list = []
        #TODO: should we maintain sentence structure or only use one string for the whole input?
        for sent in phrased:
            phrased_list.extend(sent.split(' '))
        phrased_token_list = []
        phrase_index = 0
        print(str(normalized_tokens))
        print(str(phrased_list))
        for i, token in enumerate(normalized_tokens):
            if phrase_index >= len(phrased_list):
                # phrased is finished, last token from normalized list left
                phrased_token_list.append(token)
            elif token.name == phrased_list[phrase_index]:
                phrased_token_list.append(token)
            elif isinstance(token, TagToken):
                phrased_token_list.append(token)
                phrase_index -= 1
            elif phrased_list[phrase_index].startswith('<'):
                # we have a new tag token from the phrasing module
                tag_tok = TagToken(phrased_list[phrase_index], token.token_index)
                phrased_token_list.append(tag_tok)
                # if we have a 'pure' punctuation token, do nothing further, but if the tag-token was added
                # in between tokens as a result of phrasing, add the normalized token to the list as well
                if not self.is_punct(token):
                    phrased_token_list.append(token)
                    phrase_index += 1

            phrase_index += 1
        return phrased_token_list

    def add_pause_tags(self, normalized_tokens: list) -> list:
        """Instead of performing a phrasing analysis, this is a short-cut to only insert pause tags
        for punctuation marks left in the normalized token list."""

        phrased_token_list = []
        for i, token in enumerate(normalized_tokens):
            if isinstance(token, TagToken):
                phrased_token_list.append(token)
            elif self.is_punct(token):
                tag_tok = TagToken(SIL_TAG, token.token_index)
                phrased_token_list.append(tag_tok)
            else:
                phrased_token_list.append(token)

        return phrased_token_list
