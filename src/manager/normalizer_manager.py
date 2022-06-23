"""
Handles the communication with the normalizer module. The result of the normalize methods in normalizer_manager is
a list of NormalizedTokens, composed from the original tokens, possibly a cleaned version, and the normalized
version. The list will also possibly contain TagTokens, created from SSML-tags inserted by the cleaner module or
the normalizer module, as well as pos-tags delivered by the normalizer module.
"""
import difflib
import re
from typing import Union, Tuple
from .tokens import Token, CleanToken, NormalizedToken, TagToken, Normalized
from .tokens_manager import extract_text, extract_sentences_by_tokens
from .linked_tokens import LinkedTokens
#production
#from regina_normalizer import abbr_functions
#from regina_normalizer import number_functions
#local testing
from src.regina_normalizer.regina_normalizer_pkg.regina_normalizer import abbr_functions
from src.regina_normalizer.regina_normalizer_pkg.regina_normalizer import number_functions


class NormalizerManager:


    def extract_prenorm_tuples(self, prenorm_arr, sent):
        """
        Find changes in prenorm_sent compared to sent and create tuples with original token and expanded abbreviation
        Example:
        sent == Það voru t.d. 5 atriði
        prenorm_sent == Það voru til dæmis 5 atriði

        return [('Það', 'Það'), ('voru', 'voru'), ('t.d.', 'til dæmis'), ('5', '5), ('atriði', 'atriði')]
        :param prenorm_sent:
        :param sent:
        :return:
        """
        norm_tuples = []
        sent_arr = sent.split()

        diff = difflib.ndiff(sent_arr, prenorm_arr)
        # a token from sent_arr not occurring in the prenorm_arr, store while processing the same/near positions in prenorm_arr
        current_key = ''
        # a token from prenorm_arr not occurring in the sent_arr, store while processing the same/near positions in sent_arr
        current_value = ''

        for elem in diff:
            if elem[0] == ' ':
                if current_key and current_value:
                    # add the orignal (key) - prenorm (value) tuple to the results
                    norm_tuples.append((current_key.strip(), current_value.strip()))
                    current_key = ''
                    current_value = ''
                norm_tuples.append((elem[2:], elem[2:]))
            elif elem[0] == '-':
                # elem in list1 but not in list2
                current_key += ' ' + str(elem[2:])
            elif elem[0] == '+':
                # elem in list2 but not in list1
                current_value += ' ' + str(elem[2:])
        if current_key and current_value:
            norm_tuples.append((current_key.strip(), current_value.strip()))

        return norm_tuples

    def normalize(self, text: str) -> Tuple:
        abbr_sent = abbr_functions.replace_abbreviations(text, "other")
        prenorm_tuples = self.extract_prenorm_tuples(abbr_sent, text)
        expanded_abbr = ' '.join(abbr_sent)
        normalized = number_functions.handle_sentence(expanded_abbr.strip(), "other")

        return prenorm_tuples, normalized

    def init_normalized(self, token: Union[Token, CleanToken], word: str, pos: str) -> Union[TagToken, NormalizedToken]:

        if word.startswith('<'):
            norm_tok = TagToken(word.strip(), token.token_index) # only take simple tags like '<sil>' into account at this stage
        else:
            norm_tok = NormalizedToken(token)
            norm_tok.set_normalized(word.strip())
            norm_tok.set_pos(pos)
        return norm_tok

    def normalize_token_list(self, token_list: list) -> list:
        """Normalizes the text represented by the token list,
        assembles a new list of NormalizedTokens and TagTokens, if any are in the token list or if tags are added
        during normalization."""

        pre_normalized = []
        final_normalized = []
        text_arr = extract_sentences_by_tokens(token_list)
        for sent in text_arr:
            pre, final = self.normalize(sent)
            pre_normalized.extend(pre)
            final_normalized.extend(final)

        pre_norm_linked = LinkedTokens()
        pre_norm_linked.init_from_prenorm_tuples(pre_normalized)
        norm_linked = LinkedTokens()
        norm_linked.init_from_norm_tuples(final_normalized)
        normalized_tokens = self.align_normalized(token_list, pre_norm_linked, norm_linked)
        return normalized_tokens

    def align_normalized(self, token_list, pre_normalized, final_normalized):
        normalized_tokens = []
        i = 0
        current_prenorm = pre_normalized.head
        current_norm = final_normalized.head
        # iterate through the original tokens
        while i < len(token_list):
            tok = token_list[i]
            if isinstance(tok, TagToken):
                normalized_tokens.append(tok)
                i += 1
                continue
            else:
                original_token = ' '.join(tok.tokenized)
                if not original_token:
                    # TODO: what does this represent? We have something normalized but no original token name?
                    normalized_tokens.append(tok)
                # (2021,2021) vs. (2021, tvö þúsund tuttugu og eitt)
                elif current_norm.token == original_token and len(current_norm.processed.split()) > 1:
                    normalized_arr = []
                    for wrd in current_norm.processed.split():
                        punct = ''
                        if wrd.endswith(',') or wrd.endswith('.'):
                            punct = wrd[-1]
                            wrd = wrd[:-1]
                        if wrd:
                            if wrd.startswith('<'):
                                normalized = Normalized(wrd, 'TAG')
                            else:
                                normalized = Normalized(wrd, current_norm.pos)
                            normalized_arr.append(normalized)
                        if punct:
                            # for IceParser the pos of a puncutation char is the punctuation char itself
                            normalized = Normalized(punct, punct)
                            normalized_arr.append(normalized)
                    tok.set_normalized(normalized_arr)
                    normalized_tokens.append(tok)
                    current_norm.visited = True

                # (10,10) vs. (10, tíu, ta)
                elif current_norm.token == original_token:
                    wrd = current_norm.processed.strip()
                    punct = ''
                    normalized_arr = []
                    if wrd.endswith(',') or wrd.endswith('.'):
                        punct = wrd[-1]
                        wrd = wrd[:-1]
                    if wrd:
                        if wrd.startswith('<'):
                            normalized = Normalized(wrd, 'TAG')
                        else:
                            normalized = Normalized(wrd, current_norm.pos)
                        normalized_arr.append(normalized)
                    if punct:
                        # for IceParser the pos of a puncutation char is the punctuation char itself
                        normalized = Normalized(punct, punct)
                        normalized_arr.append(normalized)
                    tok.set_normalized(normalized_arr)
                    normalized_tokens.append(tok)
                    current_norm.visited = True


                # (-,til) vs. (til, til)
                elif current_prenorm.token == original_token and current_norm.token == current_prenorm.processed:
                    wrd = current_norm.processed.strip()
                    punct = ''
                    normalized_arr = []
                    if wrd.endswith(',') or wrd.endswith('.'):
                        punct = wrd[-1]
                        wrd = wrd[:-1]
                    if wrd:
                        if wrd.startswith('<'):
                            normalized = Normalized(wrd, 'TAG')
                        else:
                            normalized = Normalized(wrd, current_norm.pos)
                        normalized_arr.append(normalized)
                    if punct:
                        # for IceParser the pos of a puncutation char is the punctuation char itself
                        normalized = Normalized(punct, punct)
                        normalized_arr.append(normalized)
                    tok.set_normalized(normalized_arr)
                    normalized_tokens.append(tok)
                    current_norm.visited = True

                # (m/s,metrar á sekúndu) vs. (metrar, metrar, nkfn) (á, á, af), (sekúndu, sekúndu, nveþ)
                # -> three tokens with original 'm/s' and the same index as 'm/s'
                elif current_prenorm.token == original_token and len(current_prenorm.processed.split()) > 1:
                    normalized_arr = []
                    for j, wrd in enumerate(current_prenorm.processed.split()):
                        if current_norm.token == wrd:
                            norm_wrd = current_norm.processed
                            punct = ''
                            if norm_wrd.endswith(',') or norm_wrd.endswith('.'):
                                punct = norm_wrd[-1]
                                norm_wrd = norm_wrd[:-1]
                            if norm_wrd:
                                if norm_wrd.startswith('<'):
                                    normalized = Normalized(norm_wrd, 'TAG')
                                else:
                                    normalized = Normalized(norm_wrd, current_norm.pos)
                                normalized_arr.append(normalized)
                            if punct:
                                # for IceParser the pos of a puncutation char is the punctuation char itself
                                normalized = Normalized(punct, punct)
                                normalized_arr.append(normalized)
                            if current_norm.next:
                                current_norm = current_norm.next
                        else:
                            break
                    tok.set_normalized(normalized_arr)
                    normalized_tokens.append(tok)

                # the tokenizer has split up the original token, so the original token tokenized spans more than
                # one entry in pre_normalized
                # Example: 10-12 gets split up into 10 - 12
                elif original_token.startswith(current_prenorm.token):
                    normalized_arr = []
                    for j in range(len(tok.tokenized)):
                        # did the pre-norm process split up the token in tok.tokenized?
                        no_prenorm_tokens = len(current_prenorm.processed.split())
                        if no_prenorm_tokens > 1:
                            original_arr = original_token.split()
                            original_tok_rest = ''.join(original_arr[j:])
                            pre_norm_arr = current_prenorm.processed.split()
                            pre_norm_str = ''.join(pre_norm_arr)
                            if original_tok_rest.startswith(pre_norm_str):
                                for k in range(no_prenorm_tokens):
                                    norm_wrd = current_norm.processed.strip()
                                    current_norm.visited = True
                                    punct = ''
                                    if norm_wrd.endswith(',') or norm_wrd.endswith('.'):
                                        punct = norm_wrd[-1]
                                        norm_wrd = norm_wrd[:-1]
                                    if norm_wrd:
                                        if norm_wrd.startswith('<'):
                                            normalized = Normalized(norm_wrd, 'TAG')
                                        else:
                                            normalized = Normalized(norm_wrd, current_norm.pos)
                                        normalized_arr.append(normalized)
                                    if punct:
                                        # for IceParser the pos of a puncutation char is the punctuation char itself
                                        normalized = Normalized(punct, punct)
                                        normalized_arr.append(normalized)

                                    if current_norm.next:
                                        current_norm = current_norm.next
                                    else:
                                        break
                            else:
                                print('original_token: ' + original_token)
                                print('prenormalized: ' + current_prenorm.processed)

                        else:
                            norm_wrd = current_norm.processed.strip()
                            current_norm.visited = True
                            punct = ''
                            if norm_wrd.endswith(',') or norm_wrd.endswith('.'):
                                punct = norm_wrd[-1]
                                norm_wrd = norm_wrd[:-1]
                            if norm_wrd:
                                if norm_wrd.startswith('<'):
                                    normalized = Normalized(norm_wrd, 'TAG')
                                else:
                                    normalized = Normalized(norm_wrd, current_norm.pos)
                                normalized_arr.append(normalized)
                            if punct:
                                # for IceParser the pos of a puncutation char is the punctuation char itself
                                normalized = Normalized(punct, punct)
                                normalized_arr.append(normalized)

                        if current_prenorm.next:
                            current_prenorm = current_prenorm.next
                        if current_norm.visited and current_norm.next:
                            current_norm = current_norm.next

                    tok.set_normalized(normalized_arr)
                    normalized_tokens.append(tok)
                    current_prenorm = current_prenorm.previous

                # no change in normalization
                else:
                    tok.set_normalized([Normalized(current_norm.processed,
                                           current_norm.pos)])
                    normalized_tokens.append(tok)

            i += 1
            if current_prenorm.next:
                current_prenorm = current_prenorm.next
            if current_norm.next:
                if current_norm.visited:
                    current_norm = current_norm.next
            elif not current_norm.visited:
                pass
            else:
                break

        return normalized_tokens
