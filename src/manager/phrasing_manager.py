"""
Handles the communication with the phrasing module. The result of the phrasing methods in phrasing_manager is
a list of NormalizedTokens, the same as the input from the normalizer_manager. The phrasing module adds TagTokens
where it assumes a good place for a speech pause.
"""
import os
from .tokens import Token, TagToken
from .tokens_manager import extract_tagged_text
from phrasing.phrasing import Phrasing

# used to replace punctuation in normalized text if we don't perform real phrasing analysis
SIL_TAG = '<sil>'


class PhrasingManager:

    @staticmethod
    def is_punct(tok: Token):
        if isinstance(tok, TagToken):
            return False
        for normalized in tok.normalized:
            if normalized.pos in ['.', ',', 'pg', 'pa', 'pl'] or tok.name == '/':
                return True
        return False

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

        for i, token in enumerate(normalized_tokens):
            if phrase_index >= len(phrased_list):
                # phrased is finished, last token from normalized list left
                phrased_token_list.append(token)
            elif token.name == phrased_list[phrase_index] or token.name.replace('-', '<pau>') == phrased_list[phrase_index]:
                # TODO: <pau> tag should not be embedded in a token! check phrasing module
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
            elif not token.name:
                # if token.name is empty, it contains a token in the originalToken that has been
                # deleted during cleaning, need to keep the token anyway
                phrased_token_list.append(token)
                phrase_index -= 1
            else:
                # check for 1 to n relation phrased vs. normalized
                # e.g. 'fimm' vs. 'fimm fimm sjö <sil> einn tveir þrír fjórir'
                normalized = token.name
                norm_arr = normalized.split('<sil>')
                if len(norm_arr) > 1:
                    # we have a <sil> tag somewhere in the normalized name
                    for str in norm_arr:
                        norm_token = NormalizedToken(token.clean_token)
                        norm_token.set_normalized(str)
                        norm_token.set_index(token.token_index)
                        norm_token.set_pos(token.pos)
                        tag_tok = TagToken('<sil>', token.token_index)
                        phrased_token_list.append(norm_token)
                        phrased_token_list.append(tag_tok)
                    # remove the last '<sil>' token
                    phrased_token_list = phrased_token_list[:-1]
                else:
                    phrased_token_list.append(token)

                phrase_index += len(normalized.split())
                i += len(normalized.split())

            phrase_index += 1
        return phrased_token_list

    def add_pause_tags(self, normalized_tokens: list) -> list:
        """Instead of performing a phrasing analysis, this is a short-cut to only insert pause tags
        for punctuation marks left in the normalized token list."""

        phrased_token_list = []
        for i, token in enumerate(normalized_tokens):
            if self.is_punct(token):
                if len(token.normalized) > 1:
                    phrased_token_list.append(token)
                tag_tok = TagToken(SIL_TAG, token.token_index)
                phrased_token_list.append(tag_tok)
            else:
                phrased_token_list.append(token)

        return phrased_token_list
