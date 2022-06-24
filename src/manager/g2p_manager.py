"""
Handles the communication with the g2p module. The result of the g2p methods in g2p_manager is
a string in an input format for a TTS system. Following formats are supported:
...
...
"""
import os

from .tokens import Token, Normalized, TagToken
from ice_g2p.transcriber import Transcriber, G2P_METHOD


SIL_TOKEN = '<sil>'
ENGLISH = 'enska'


class G2PManager:

    def __init__(self):
        self.g2p = Transcriber(G2P_METHOD.FAIRSEQ, lang_detect=True, use_dict=True)
        self.syllab_symbol = ''
        self.stress = False
        self.word_separator = ''

    def set_core_pron_dict(self, pron_dict: dict):
        self.g2p.override_core_dict(pron_dict)

    def set_custom_dict(self, pron_dict: dict):
        self.g2p.set_custom_dict(pron_dict)

    def set_syllab_symbol(self, syllab_symbol: str):
        self.g2p.syllab_symbol = syllab_symbol

    def set_stress(self, value: bool):
        self.g2p.add_stress_label = value

    def set_word_separator(self, word_sep: str):
        self.g2p.word_separator = word_sep

    def generate_normalized(self, word: str, token_ind: int) -> Token:
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
        base_token.set_tokenized([base_token])
        base_token.set_normalized([Normalized(word, 'n')])
        return base_token

    def transcribe(self, token_list: list) -> list:
        """Transcribes the tokens in token_list and returns a list of
        transcribedTokens, keeps the tagTokens already in the input token_list, except for
        the lang-SSML tag, which is used to transcribe English words using English g2p"""

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
                    normalized = self.generate_normalized(ENGLISH, token.token_index)
                    transcribed = self.g2p.transcribe(ENGLISH)
                    normalized.set_transcribed([transcribed])
                    transcribed_list.append(normalized)
                    transcribed_list.append(TagToken(SIL_TOKEN, token.token_index))
                elif token.ssml_end:
                    is_icelandic = True
                    transcribed_list.append(TagToken(SIL_TOKEN, token.token_index))
                else:
                    transcribed_list.append(token)
            else:
                transcribed_arr = []
                if token.normalized:
                    for norm in token.normalized:
                        transcribed = self.g2p.transcribe(norm.norm_str.lower().strip(), icelandic=is_icelandic)
                        transcribed_arr.append(transcribed)
                token.set_transcribed(transcribed_arr)
                transcribed_list.append(token)

        return transcribed_list

