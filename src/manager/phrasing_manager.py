"""
Handles the communication with the phrasing module. The result of the phrasing methods in phrasing_manager is
a list of NormalizedTokens, the same as the input from the normalizer_manager. The phrasing module adds TagTokens
where it assumes a good place for a speech pause.
"""
import os
import time
from tokens import TagToken
from tokens_manager import extract_tagged_text
from phrasing.phrasing import Phrasing


class PhrasingManager:

    def phrase_text(self, tagged_text: str):
        MANAGER_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
        PROJECT_ROOT, tail = os.path.split(MANAGER_PROJECT_ROOT)
        os.chdir(PROJECT_ROOT + '/manager/IceNLP/bat/iceparser')
        print('PROJECT_ROOT: ' + PROJECT_ROOT)
        start1 = time.time()
        with open('tagged_tmp.txt', 'w') as f:
            f.write(tagged_text)
        start2 = time.time()
        comm = './iceparser.sh -i tagged_tmp.txt -o ../../../parsed_tmp.txt'
        os.system(comm)
        os.remove('tagged_tmp.txt')
        os.chdir(PROJECT_ROOT)
        start3 = time.time()
        with open(PROJECT_ROOT + '/manager/parsed_tmp.txt') as file:
            lines = [line.strip() for line in file]
        start4 = time.time()
        phraser = Phrasing()
        paused_text = phraser.insert_pauses(lines)
        start5 = time.time()
        os.remove(PROJECT_ROOT + '/manager/parsed_tmp.txt')

        # Timing results:
        """
        print('writing tagged text: ' + str(start2 - start1))
        print('parsing tagged text: ' + str(start3 - start2))
        print('read parsed text: ' + str(start4 - start3))
        print('phrase text: ' + str(start5 - start4))
        print('total time phrasing: ' + str(start5 - start1))
        """
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
            if token.name == phrased_list[phrase_index]:
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
                if token.pos != '.' and token.pos != ',' and token.pos != 'pg' and token.name != '/':
                    phrased_token_list.append(token)
                    phrase_index += 1

            phrase_index += 1
        return phrased_token_list
