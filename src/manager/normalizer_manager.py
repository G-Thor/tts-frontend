"""
Handles the communication with the normalizer module. The result of the normalize methods in normalizer_manager is
a list of NormalizedTokens, composed from the original tokens, possibly a cleaned version, and the normalized
version. The list will also possibly contain TagTokens, created from SSML-tags inserted by the cleaner module or
the normalizer module, as well as pos-tags delivered by the normalizer module.
"""
import difflib
from typing import Union, Tuple
from .tokens import Token, CleanToken, NormalizedToken, TagToken
from .tokens_manager import extract_text, extract_sentences
#production
from regina_normalizer import abbr_functions
from regina_normalizer import number_functions
#local testing
#from src.regina_normalizer.regina_normalizer_pkg.regina_normalizer import abbr_functions
#from src.regina_normalizer.regina_normalizer_pkg.regina_normalizer import number_functions


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
        # TODO: refactor, extract methods
        normalized_tokens = []
        pre_normalized = []
        final_normalized = []
        text_arr = extract_sentences(token_list)
        for sent in text_arr:
            pre, final = self.normalize(sent)
            pre_normalized.extend(pre)
            final_normalized.extend(final)

        pre_norm_index = 0
        norm_index = 0
        i = 0
        # iterate through the original tokens
        while i < len(token_list):
            tok = token_list[i]
            norm_index_counter = 0 # indicates how many indices further we move internally in the normalized list during each iteration
            if isinstance(tok, TagToken):
                normalized_tokens.append(tok)
                norm_index -= 1 # normalized token list does not contain the tagTokens, so we need to go back with the index
                pre_norm_index -= 1
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
                elif pre_normalized[pre_norm_index][0] == original_token and normalized_base_token == pre_normalized[pre_norm_index][1]:
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
                elif pre_normalized[pre_norm_index][0] == original_token and len(pre_normalized[pre_norm_index][1].split()) > 1:
                    for j, wrd in enumerate(pre_normalized[pre_norm_index][1].split()):
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
                elif original_token != pre_normalized[pre_norm_index][0]:
                    # we have some changes during pre-normalization, e.g. from '570 1234' -> '570-1234'
                    # so we need to reconstruct the original and clean tokens
                    new_clean = pre_normalized[pre_norm_index][0]
                    new_original = Token(pre_normalized[pre_norm_index][0])
                    new_original.set_index(tok.token_index)
                    span_start = tok.get_original_token().start
                    span_end = tok.get_original_token().end
                    new_token_name = original_token
                    while new_original.name != new_token_name:
                        if isinstance(token_list[i + 1], TagToken):
                            normalized_tokens.append(tok)
                            norm_index -= 1
                            pre_norm_index -= 1
                            break
                        else:
                            i += 1
                            continued_token = token_list[i]
                            new_token_name += ' ' + continued_token.name
                            span_end = continued_token.get_original_token().end
                    new_original.set_span(span_start, span_end)
                    new_clean_tok = CleanToken(new_original)
                    new_clean_tok.set_clean(new_clean)
                    new_clean_tok.set_index(new_original.token_index)
                    norm_tok = self.init_normalized(new_original, final_normalized[norm_index][1], final_normalized[norm_index][2])
                    normalized_tokens.append(norm_tok)
                    #counter_subtraction = len(new_original.name.split()) - 1
                    #pre_norm_index -= counter_subtraction
                    #norm_index -= counter_subtraction
                    #i += 1

                # no change in normalization
                else:
                    norm_tok = self.init_normalized(tok, final_normalized[norm_index][1],
                                           final_normalized[norm_index][2])
                    normalized_tokens.append(norm_tok)

            i += 1
            pre_norm_index += 1
            norm_index += norm_index_counter + 1

        return normalized_tokens

