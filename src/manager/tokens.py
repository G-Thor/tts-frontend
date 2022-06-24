"""
Various token classes to hold information from the text processing pipeline.

"""

import json
from typing import Union


class Token:

    def __init__(self, name: str):
        self.name = name
        self.token_index = -1
        self.start = -1
        self.end = -1
        self.clean = ''
        self.tokenized = []
        self.normalized = []
        self.transcribed = []
        self.nsw = False

    def __repr__(self):
        return f"\nToken:\n" \
               f"Original: {self.name}, Clean: {self.clean},\n" \
               f"Tokenized: {self.tokenized},\n" \
               f"Normalized: {str(self.normalized)}\n" \
               f"Transcribed: {str(self.transcribed)}\n" \
               f"index: {self.token_index}, {self.start}, {self.end}\n"

    def __str__(self):
        return f"\nToken:\n" \
               f"Original: {self.name}, Clean: {self.clean},\n" \
               f"Tokenized: {self.tokenized},\n" \
               f"Normalized: {str(self.normalized)}\n" \
               f"Transcribed: {str(self.transcribed)}\n" \
               f"index: {self.token_index}, {self.start}, {self.end}\n"

    def __eq__(self, other):
        if isinstance(other, Token):
            return other.name == self.name and other.token_index == self.token_index
        return False

    def to_json(self):
        return json.dumps(self, ensure_ascii=False, default=lambda o: o.__dict__, indent=4)

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

    def set_normalized(self, normalized: list):
        """Add a list of normalized objects generated from base token."""
        self.normalized = normalized

    def set_transcribed(self, transcribed: list):
        """Add a list of normalized objects generated from base token."""
        self.transcribed = transcribed


class Normalized:

    def __init__(self, normalized: str, pos: str):
        self.norm_str = normalized
        self.pos = pos

    def __repr__(self):
        return f"{self.norm_str}, {self.pos}"

    def __str__(self):
        return f"{self.norm_str}, {self.pos}"

    def __eq__(self, other):
        if isinstance(other, Normalized):
            return other.norm_str == self.norm_str and other.pos == self.pos
        return False


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

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)
