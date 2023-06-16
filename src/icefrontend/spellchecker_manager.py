from reynir_correct.tools import tts_frontend
from .tokens import Token, TagToken
from .tokens_manager import extract_sentences_by_normalized
from .settings import SENTENCE_TAG

class SpellCheckerManager:
    """
    Connects with the GreynirCorrect4LT package to spell correct normalized text.
    Replaces normalized text with spell corrected, if applicable.
    """
    def spellcheck(self, text):
        checked = tts_frontend.tts_spellcheck(text)
        print(checked)

    def spellcheck_token_list(self, tokens: list) -> list:
        sentences = extract_sentences_by_normalized(tokens)
        checked_sentences = []
        for sent in sentences:
            checked_sentences.extend(tts_frontend.tts_spellcheck(sent).split())

        spellchecked_normalized = []
        for token in tokens:
            if isinstance(token, TagToken):
                spellchecked_normalized.append(token)
            else:
                # processed_token_count tells us how many of the tokens in checked_sentences were processed
                # when comparing to the normalized version of token
                processed_token_count = token.update_spellchecked(checked_sentences)
                spellchecked_normalized.append(token)
                checked_sentences = checked_sentences[processed_token_count:]

        return spellchecked_normalized
