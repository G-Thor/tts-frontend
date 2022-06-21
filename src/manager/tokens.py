"""
Various token classes to hold information from the text processing pipeline.

"""

from typing import Union


class Token:

    def __init__(self, name: str):
        self.name = name
        self.token_index = -1
        self.start = -1
        self.end = -1
        self.tokenized = []
        self.nsw = False

    def __repr__(self):
        return f"\nToken:\n" \
               f"Original: {self.name}, Clean: {self.clean},\n" \
               f"Tokenized: {self.tokenized},\n" \
               f"index: {self.token_index}, {self.start}, {self.end}\n"

    def __str__(self):
        return f"\nToken:\n" \
               f"Original: {self.name}, Clean: {self.clean},\n" \
               f"Tokenized: {self.tokenized},\n" \
               f"index: {self.token_index}, {self.start}, {self.end}\n"

    def __eq__(self, other):
        if isinstance(other, Token):
            return other.name == self.name and other.token_index == self.token_index
        return False

    def set_index(self, ind: int):
        """Index of the token in text."""
        self.token_index = ind

    def set_span(self, start: int, end: int):
        """Span in text, from and including start to and excluding end."""
        self.start = start
        self.end = end

    def set_clean(self, clean: str):
        """Add a cleaned version of the original token"""
        # TODO: is this ever more than one token?
        self.clean = clean

    def set_tokenized(self, tokens: list):
        """Add a list of tokens generated from base token. We only have more than one token for NSWs"""
        self.tokenized = tokens


class CleanToken:

    def __init__(self, original: Token):
        """A cleaned token might be the same as the original token, both in terms of the token string
        and the index. On intialization we set this object's name and index to be that of the original token."""
        self.original_token = original
        self.name = original.name
        self.token_index = original.token_index

    def __repr__(self):
        return f"CleanToken({self.original_token.name}, {self.name}, {self.token_index})"

    def __str__(self):
        return f"CleanToken: original: {self.original_token.name}, " \
               f"clean: {self.name}, index: {self.token_index}"

    def __eq__(self, other):
        if isinstance(other, CleanToken):
            return other.name == self.name and other.token_index == self.token_index
        return False

    def set_clean(self, clean: str):
        self.name = clean

    def set_index(self, ind: int):
        self.token_index = ind

    def get_original_token(self) -> Token:
        return self.original_token


class NormalizedToken:
    """A normalized token gets overridden in the spell checker if the spell checker is used.
    Normalized token will be the spell corrected, normalized token, and the part-of-speech (pos) will
    possibly be overridden by the pos of the spell corrected token."""

    def __init__(self, original: Union[Token, CleanToken]):
        if isinstance(original, Token):
            # if we are initializing a normalized token directly from an original token,
            # we need to init a clean token with the same information as well to prevent
            # things from breaking at later stages, i.e. a normalized token is always
            # assumed to contain a clean token
            self.original_token = original
            self.clean_token = CleanToken(original)
        else:
            self.original_token = original.get_original_token() # do we need this?
            self.clean_token = original
        self.name = self.original_token.name
        self.token_index = self.original_token.token_index
        self.pos = '' #TODO: use some kind of default pos-tag like 'unk'?

    def __repr__(self):
        return f"NormalizedToken({self.original_token.name}, {self.name}, {self.token_index})"

    def __str__(self):
        return f"NormalizedToken: original: {self.original_token.name}, " \
               f"normalized: {self.name}, index: {self.token_index}"

    def __eq__(self, other):
        if isinstance(other, NormalizedToken):
            return other.name == self.name and other.token_index == self.token_index
        return False

    def set_normalized(self, norm: str):
        self.name = norm

    def set_index(self, ind: int):
        self.token_index = ind

    def set_pos(self, pos: str):
        self.pos = pos


class TranscribedToken:

    def __init__(self, original: NormalizedToken):
        self.normalized = original
        self.name = ''

    def __repr__(self):
        return f"TranscribedToken({self.normalized.name}, {self.name}, {self.normalized.token_index})"

    def __str__(self):
        return f"TranscribedToken: original: {self.normalized.name}, " \
               f"transcribed: {self.name}, index: {self.normalized.token_index}"

    def __eq__(self, other):
        if isinstance(other, NormalizedToken):
            return other.name == self.name and other.token_index == self.normalized.token_index
        return False

    def set_transcribed(self, transcr: str):
        self.name = transcr

    def get_original_token(self) -> Token:
        return self.normalized.original_token


class TagToken:
    """This token is different from the (processed) text token classes in that it does not
    hold information about a text token but on a tag, like SSML-tag or pause tags. It can be
    an enclosing tag (<> ... </>) or a single tag. Default is a non-enclosing, single tag token."""

    def __init__(self, name: str, ind: int):
        self.name = name
        self.token_index = ind # position in text token collection
        # if this is an ssml start or end tag, set values in set_ssml_start/set_ssml_end as appropriate
        self.ssml_start = False
        self.ssml_end = False

    def set_ssml_start(self, start: bool):
        self.ssml_start = start

    def set_ssml_end(self, end: bool):
        self.ssml_end = end

    def __repr__(self):
        return f"TagToken({self.name}, {self.token_index})"

    def __str__(self):
        return f"TagToken: tag: {self.name}, index: {self.token_index}"
