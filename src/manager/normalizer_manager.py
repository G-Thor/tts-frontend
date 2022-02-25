"""
Handles the communication with the normalizer module. The result of the normalize methods in normalizer_manager is
a list of NormalizedTokens, composed from the original tokens, possibly a cleaned version, and the normalized
version. The list will also possibly contain TagTokens, created from SSML-tags inserted by the cleaner module or
the normalizer module, as well as pos-tags delivered by the normalizer module.
"""
from typing import Union
from tokens import Token, CleanToken, NormalizedToken, TagToken
from tokens_manager import extract_text
from regina_normalizer import abbr_functions
from regina_normalizer import number_functions


def normalize(text: str) -> str:
    abbr_sent = abbr_functions.replace_abbreviations(text, "sport")
    expanded_abbr = ''
    for tup in abbr_sent:
        expanded_abbr += tup[1] + ' '
    normalized = number_functions.handle_sentence(expanded_abbr.strip(), "sport")

    return normalized


def init_normalized(token: Union[Token, CleanToken], word: str, pos: str) -> Union[TagToken, NormalizedToken]:

    if word.startswith('<'):
        norm_tok = TagToken(word, token.token_index) # only take simple tags like '<sil>' into account at this stage
    else:
        norm_tok = NormalizedToken(token)
        norm_tok.set_normalized(word)
        norm_tok.set_pos(pos)
    return norm_tok


def normalize_token_list(token_list: list) -> list:
    """Normalizes the text represented by the token list,
    assembles a new list of NormalizedTokens and TagTokens, if any are in the token list or if tags are added
    during normalization."""
    normalized_tokens = []
    text = extract_text(token_list)
    normalized = normalize(text)
    norm_index = 0
    for i, tok in enumerate(token_list):
        if isinstance(tok, TagToken):
            normalized_tokens.append(tok)
            norm_index -= 1 # normalized token list does not contain the tagTokens, so we need to go back with the index
        else:
            norm_words = normalized[norm_index][1].strip().split(' ')
            for wrd in norm_words:
                punct = ''
                if wrd.endswith(',') or wrd.endswith('.'):
                    punct = wrd[-1]
                    wrd = wrd[:-1]
                if wrd:
                    norm_tok = init_normalized(tok, wrd, normalized[norm_index][2])
                    normalized_tokens.append(norm_tok)
                if punct:
                    # for IceParser the pos of a puncutation char is the punctuation char itself
                    punct_tok = init_normalized(tok, punct, punct)
                    normalized_tokens.append(punct_tok)
        norm_index += 1

    return normalized_tokens
