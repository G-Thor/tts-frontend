"""
Handles the communication with the text-cleaner module. The result of the cleaning methods in cleaner_manager is
a list of CleanTokens, composed from the original tokens in the input and the cleaned version. The list will also
possibly contain TagTokens, created from SSML-tags inserted by the cleaner module.

"""

from typing import Tuple

from .settings import (
    HTML_CLOSING_TAG_REPL,
    PUNCTUATION,
    VALID_CHARACTERS,
)

from .tokens import CleanToken, TagToken
from .tokens_manager import init_tokens
from text_cleaner import TextCleaner
from text_cleaner import HtmlCleaner

SSML_LANG_START = '<lang'
SSML_LANG_END = '</lang>'


class CleanerManager:
    """Connects the pipeline to the text-cleaner module and manages input and output"""

    def __init__(self, repl_dict: dict, post_lookup_dict: dict):
        self.cleaner = TextCleaner(replacement_dict=repl_dict, post_dict=post_lookup_dict, punct_set=PUNCTUATION)
        self.html_cleaner = HtmlCleaner()

    def clean_text(self, text: str) -> list:
        """The text attribute should be raw text, i.e. not html. Returns a list of CleanTokens."""
        token_list = init_tokens(text)
        clean_tokens = []
        for tok in token_list:
            cleaned = self.cleaner.clean(tok.name)
            clean_token = CleanToken(tok)
            clean_token.set_clean(cleaned)
            clean_tokens.append(clean_token)

        return clean_tokens

    def create_token_lists(self, html_string: str) -> Tuple[list, list]:
        """Extract raw tokens list and clean tokens list from html_string."""

        raw_text = self.html_cleaner.clean_html(html_string)
        cleaned = self.cleaner.clean(raw_text)
        token_list = init_tokens(raw_text)
        clean_tokens = init_tokens(cleaned)
        return token_list, clean_tokens

    def html_to_raw(self, html_string: str):
        """The html parser is designed around the EPUB-format and will parse the html_string accordingly.
        Returns a raw string representation of the html content"""

        return self.clean_html_text(html_string)

    def clean_html_text(self, html_string: str) -> list:
        """The html parser is designed around the EPUB-format and will parse the html_string accordingly.
        Returns a list of CleanTokens, with TagTokens if any SSML-tags were created by the cleaner."""

        orig_tokens, clean_tokens = self.create_token_lists(html_string)
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
