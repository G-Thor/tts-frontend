"""
Handles the communication with the text-cleaner module. The result of the cleaning methods in cleaner_manager is
a list of CleanTokens, composed from the original tokens in the input and the cleaned version. The list will also
possibly contain TagTokens, created from SSML-tags inserted by the cleaner module.

"""

from typing import Tuple

from tokens import CleanToken, TagToken
from tokens_manager import init_tokens
from text_cleaner import clean
from text_cleaner import clean_html_string

SSML_LANG_START = '<lang'
SSML_LANG_END = '</lang>'


def clean_text(text: str, alphabet: list, punct_set: list) -> list:
    """The text attribute should be raw text, i.e. not html. Returns a list of CleanTokens."""
    token_list = init_tokens(text)
    clean_tokens = []
    for tok in token_list:
        cleaned = clean(tok.name, preserve_string=['ca'], alphabet=alphabet, punct_set=punct_set)
        clean_token = CleanToken(tok)
        clean_token.set_clean(cleaned)
        clean_tokens.append(clean_token)

    return clean_tokens


def create_token_lists(html_string: str, alphabet: list, punct_set: list) -> Tuple[list, list]:
    """Extract raw tokens list and clean tokens list from html_string."""

    raw_text = clean_html_string(html_string)
    cleaned = clean(raw_text, alphabet=alphabet, punct_set=punct_set)
    token_list = init_tokens(raw_text)
    clean_tokens = init_tokens(cleaned)
    return token_list, clean_tokens


def html_to_raw(html_string: str):
    """The html parser is designed around the EPUB-format and will parse the html_string accordingly.
    Returns a raw string representation of the html content"""

    return clean_html_string(html_string)


def clean_html_text(html_string: str, alphabet: list, punct_set: list) -> list:
    """The html parser is designed around the EPUB-format and will parse the html_string accordingly.
    Returns a list of CleanTokens, with TagTokens if any SSML-tags were created by the cleaner."""

    orig_tokens, clean_tokens = create_token_lists(html_string, alphabet, punct_set)
    clean_html_tokens = []
    clean_counter = 0
    # Create a list of CleanTokens from orig_tokens and clean_tokens.
    # Take care to insert SSML-TagTokens from clean_tokens in the correct way and adjust indices accordingly
    for i in range(len(orig_tokens)):
        orig_token = orig_tokens[i]
        clean_html_token = clean_tokens[clean_counter]
        if orig_token.name == clean_html_token.name:
            orig_token.set_index(len(clean_html_tokens))
            clean_token = CleanToken(orig_token)
            clean_token.set_clean(clean_html_token.name)
            clean_html_tokens.append(clean_token)
        else:
            if clean_html_token.name == SSML_LANG_START:
                next_clean = clean_tokens[clean_counter + 1]
                tag_str = SSML_LANG_START + ' ' + next_clean.name
                tag_tok = TagToken(tag_str, len(clean_html_tokens))
                tag_tok.ssml_start = True
                clean_html_tokens.append(tag_tok)
                clean_counter += 1
            elif clean_html_token.name.startswith(SSML_LANG_END):
                tag_tok = TagToken(SSML_LANG_END, len(clean_html_tokens))
                tag_tok.ssml_end = True
                clean_html_tokens.append(tag_tok)
                orig_token.set_index(len(clean_html_tokens))
                clean_token = CleanToken(orig_token)
                clean_token.set_clean(clean_tokens[clean_counter + 1].name)
                clean_html_tokens.append(clean_token)
                clean_counter += 1
            else:
                orig_token.set_index(len(clean_html_tokens))
                clean_token = CleanToken(orig_token)
                clean_token.set_clean(clean_html_token.name)
                clean_html_tokens.append(clean_token)
        clean_counter += 1

    return clean_html_tokens
