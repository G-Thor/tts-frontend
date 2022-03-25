"""
Handles the communication with the normalizer module. The result of the normalize methods in normalizer_manager is
a list of NormalizedTokens, composed from the original tokens, possibly a cleaned version, and the normalized
version. The list will also possibly contain TagTokens, created from SSML-tags inserted by the cleaner module or
the normalizer module, as well as pos-tags delivered by the normalizer module.
"""
from typing import Union, Tuple
from tokens import Token, CleanToken, NormalizedToken, TagToken
from tokens_manager import extract_text
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
        j = 0
        for i in range(len(sent_arr)):
            if prenorm_arr[j] == sent_arr[i]:
                norm_tuples.append((sent_arr[i], prenorm_arr[j]))
                j += 1
            else:
                abbr = sent_arr[i]
                expansion = prenorm_arr[j]
                j += 1
                while len(sent_arr) > i + 1 and sent_arr[i + 1] != prenorm_arr[j]:
                    expansion += ' ' + prenorm_arr[j]
                    j += 1
                if i == len(sent_arr) - 1:
                    while j < len(prenorm_arr):
                        expansion += ' ' + prenorm_arr[j]
                        j += 1
                norm_tuples.append((abbr, expansion))

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
        # TODO: refactor, extract methods
        normalized_tokens = []
        text = extract_text(token_list)
        pre_normalized, final_normalized = self.normalize(text)
        norm_index = 0
        # iterate through the original tokens
        for i, tok in enumerate(token_list):
            norm_index_counter = 0 # indicates how many indices further we move internally in the normalized list during each iteration
            if isinstance(tok, TagToken):
                normalized_tokens.append(tok)
                norm_index -= 1 # normalized token list does not contain the tagTokens, so we need to go back with the index

            else:
                original_token = tok.name
                normalized_base_token = final_normalized[norm_index][0]
                # (2021,2021) vs. (2021, tvö þúsund tuttugu og eitt)
                if normalized_base_token == original_token and len(final_normalized[norm_index][1].split()) > 1:
                    for wrd in final_normalized[norm_index][1].split():
                        punct = ''
                        if wrd.endswith(',') or wrd.endswith('.'):
                            punct = wrd[-1]
                            wrd = wrd[:-1]
                        if wrd:
                            norm_tok = self.init_normalized(tok, wrd,
                                                   final_normalized[norm_index][2])
                            normalized_tokens.append(norm_tok)
                        if punct:
                            # for IceParser the pos of a puncutation char is the punctuation char itself
                            punct_tok = self.init_normalized(tok, punct, punct)
                            normalized_tokens.append(punct_tok)


                # (10,10) vs. (10, tíu, ta)
                elif normalized_base_token == original_token:
                    wrd = final_normalized[norm_index][1]
                    punct = ''
                    if wrd.endswith(',') or wrd.endswith('.'):
                        punct = wrd[-1]
                        wrd = wrd[:-1]
                    if wrd:
                        norm_tok = self.init_normalized(tok, wrd,
                                               final_normalized[norm_index][2])
                        normalized_tokens.append(norm_tok)
                    if punct:
                        # for IceParser the pos of a puncutation char is the punctuation char itself
                        punct_tok = self.init_normalized(tok, punct, punct)
                        normalized_tokens.append(punct_tok)


                # (-,til) vs. (til, til)
                elif pre_normalized[i][0] == original_token and normalized_base_token == pre_normalized[i][1]:
                    wrd = final_normalized[norm_index][1]
                    punct = ''
                    if wrd.endswith(',') or wrd.endswith('.'):
                        punct = wrd[-1]
                        wrd = wrd[:-1]
                    if wrd:
                        norm_tok = self.init_normalized(tok, wrd,
                                               final_normalized[norm_index][2])
                        normalized_tokens.append(norm_tok)
                    if punct:
                        # for IceParser the pos of a puncutation char is the punctuation char itself
                        punct_tok = self.init_normalized(tok, punct, punct)
                        normalized_tokens.append(punct_tok)

                # (m/s,metrar á sekúndu) vs. (metrar, metrar, nkfn) (á, á, af), (sekúndu, sekúndu, nveþ)
                # -> three tokens with original 'm/s' and the same index as 'm/s'
                elif pre_normalized[i][0] == original_token and len(pre_normalized[i][1].split()) > 1:
                    for j, wrd in enumerate(pre_normalized[i][1].split()):
                        if final_normalized[norm_index+j][0] == wrd:
                            norm_wrd = final_normalized[norm_index+j][1]
                            punct = ''
                            if norm_wrd.endswith(',') or wrd.endswith('.'):
                                punct = norm_wrd[-1]
                                norm_wrd = norm_wrd[:-1]
                            if norm_wrd:
                                norm_tok = self.init_normalized(tok, norm_wrd,
                                                       final_normalized[norm_index + j][2])
                                normalized_tokens.append(norm_tok)
                            if punct:
                                # for IceParser the pos of a puncutation char is the punctuation char itself
                                punct_tok = self.init_normalized(tok, punct, punct)
                                normalized_tokens.append(punct_tok)

                            norm_index_counter = j

                        else:
                            break
                # no change in normalization
                else:
                    norm_tok = self.init_normalized(tok, final_normalized[norm_index][1],
                                           final_normalized[norm_index][2])
                    normalized_tokens.append(norm_tok)

            norm_index += norm_index_counter + 1

        return normalized_tokens

