"""
Handles the communication with the text-cleaner module. The result of the cleaning methods in cleaner_manager is
a list of CleanTokens, composed from the original tokens in the input and the cleaned version. The list will also
possibly contain TagTokens, created from SSML-tags inserted by the cleaner module.

"""

from .settings import PUNCTUATION

from .tokens import TagToken
from .tokens_manager import init_tokens
from text_cleaner import TextCleaner
from text_cleaner import HtmlCleaner

EN_LABEL = '(e.'
CLOSING_PAR = ')'
# SSML 1.1 standard
SSML_LANG_START = '<lang xml:lang="en-GB">'
SSML_LANG_END = '</lang>'


class CleanerManager:
    """Connects the pipeline to the text-cleaner module and manages input and output"""

    def __init__(self, repl_dict: dict, post_lookup_dict: dict, lexicon: list):
        self.cleaner = TextCleaner(replacement_dict=repl_dict, post_dict=post_lookup_dict, preserve_strings=lexicon,
                                   punct_set=PUNCTUATION)
        self.html_cleaner = HtmlCleaner()
        self.next_token_index = 0

    def clean_text(self, text: str) -> list:
        """The text attribute should be raw text, i.e. not html. Returns a list of tokens enriched with clean version
        of each token."""
        token_list = init_tokens(text)
        clean_tokens = self.clean_token_list(token_list)
        return clean_tokens

    def clean_html_text(self, html_string: str) -> list:
        """The html parser is designed around the EPUB-format and will parse the html_string accordingly.
        Returns a list of CleanTokens, with TagTokens if any SSML-tags were created by the cleaner."""
        clean_tokens = self.create_token_lists_from_html(html_string)
        return clean_tokens

    def create_token_lists_from_html(self, html_string: str) -> list:
        """Extract raw tokens list and clean tokens list from html_string."""
        raw_text = self.html_cleaner.clean_html(html_string)
        token_list = init_tokens(raw_text)
        clean_tokens = self.clean_token_list(token_list)
        return clean_tokens

    def clean_token_list(self, token_list: list) -> list:
        """Extract raw tokens list from text and enrich with a clean version."""
        lang_tag = ''
        clean_tokens = []
        for token in token_list:
            clean_tok = self.cleaner.clean(token.name)
            if clean_tok == EN_LABEL:
                lang_tag = SSML_LANG_START
                tag_tok = TagToken(lang_tag, token.token_index)
                tag_tok.ssml_start = True
                clean_tokens.append(tag_tok)
            elif clean_tok.endswith(CLOSING_PAR) and lang_tag:
                tag_tok = TagToken(SSML_LANG_END, token.token_index)
                tag_tok.ssml_end = True
                if len(clean_tok) > 1:
                    wrd = clean_tok[:-1]
                    token.set_clean(wrd)
                    clean_tokens.append(token)
                clean_tokens.append(tag_tok)
                lang_tag = ''
            else:
                token.set_clean(clean_tok)
                clean_tokens.append(token)
        return clean_tokens
