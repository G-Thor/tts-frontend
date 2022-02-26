"""
Handles the communication with the g2p module. The result of the g2p methods in g2p_manager is
a string in an input format for a TTS system. Following formats are supported:
...
...
"""
import os

from typing import Union
from tokens import TranscribedToken, TagToken
from tokens_manager import extract_tagged_text
from ice_g2p.transcriber import Transcriber, G2P_METHOD


def transcribe(token_list: list) -> list:
    """Transcribes the tokens in token_list and returns a list of
    transcribedTokens, keeps the tagTokens already in the input token_list, except for
    the lang-SSML tag, which is used to transcribe English words using English g2p"""
    g2p = Transcriber(G2P_METHOD.FAIRSEQ, True)
    transcribed_list = []
    is_icelandic = True
    for token in token_list:
        if isinstance(token, TagToken):
            # we don't add the lang-ssml tags to the g2p output, we use them to identify English
            # words in the input and replace them with <sil> tokens
            # TODO: replace with "enska" / "á ensku" ?
            if token.ssml_start:
                is_icelandic = False
                transcribed_list.append(TagToken('<sil>', token.token_index))
            elif token.ssml_end:
                is_icelandic = True
                transcribed_list.append(TagToken('<sil>', token.token_index))
            else:
                transcribed_list.append(token)
        else:
            transcribed = g2p.transcribe(token.name.lower(), is_icelandic, False, True, False)
            transcr_token = TranscribedToken(token)
            transcr_token.name = transcribed
            transcribed_list.append(transcr_token)

    return transcribed_list

