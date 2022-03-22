"""
Handles the communication with the g2p module. The result of the g2p methods in g2p_manager is
a string in an input format for a TTS system. Following formats are supported:
...
...
"""
import os

from .tokens import Token, NormalizedToken, TranscribedToken, TagToken
from ice_g2p.transcriber import Transcriber, G2P_METHOD


SIL_TOKEN = '<sil>'
ENGLISH = 'enska'


def generate_normalized(word: str, token_ind: int) -> NormalizedToken:
    """
    Generates a Token and a NormalizedToken from word and token_ind. These are not results of processing but
    inserted tokens not present in the original text, like 'enska' to announce that the following word(s) are
    in English
    :param word: the name of the new token
    :param token_ind: index of the previous token in the transcribed list
    :return: a NormalizedToken with name=word and token_index=token_ind
    """
    base_token = Token(word)
    base_token.set_index(token_ind)
    normalized = NormalizedToken(base_token)
    normalized.set_normalized(word)
    normalized.set_index(token_ind)
    return normalized


def transcribe(token_list: list, syllab_stress=False) -> list:
    """Transcribes the tokens in token_list and returns a list of
    transcribedTokens, keeps the tagTokens already in the input token_list, except for
    the lang-SSML tag, which is used to transcribe English words using English g2p"""
    g2p = Transcriber(G2P_METHOD.FAIRSEQ, True)
    transcribed_list = []
    is_icelandic = True
    for token in token_list:
        if isinstance(token, TagToken):
            # We don't add the lang-ssml tags to the g2p output, we use them to identify English
            # words in the input. Create a token 'enska' that announces the following token(s) to be
            # in English, create a '<sil>' tokens before and after the new token
            if token.ssml_start:
                is_icelandic = False
                transcribed_list.append(TagToken(SIL_TOKEN, token.token_index))
                normalized = generate_normalized(ENGLISH, token.token_index)
                transcribed = g2p.transcribe(ENGLISH, True, syllab_stress, True, False)
                transcr_token = TranscribedToken(normalized)
                transcr_token.name = transcribed
                transcribed_list.append(transcr_token)
                transcribed_list.append(TagToken(SIL_TOKEN, token.token_index))
            elif token.ssml_end:
                is_icelandic = True
                transcribed_list.append(TagToken(SIL_TOKEN, token.token_index))
            else:
                transcribed_list.append(token)
        else:
            transcribed = g2p.transcribe(token.name.lower(), is_icelandic, syllab_stress, True, False)
            transcr_token = TranscribedToken(token)
            transcr_token.name = transcribed
            transcribed_list.append(transcr_token)

    return transcribed_list

