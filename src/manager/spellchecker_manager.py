from reynir_correct.tools import tts_frontend
from .tokens import NormalizedToken, TagToken
from .tokens_manager import extract_sentences
from .settings import SENTENCE_TAG

class SpellCheckerManager:
    """
    Connects with the GreynirCorrect4LT package to spell correct normalized text.
    Replaces normalized text with spell corrected, if applicable.
    """
    def spellcheck(self, text):
        checked = tts_frontend.tts_spellcheck(text)
        print(checked)

    def spellcheck_token_list(self, normalized_tokens: list) -> list:
        sentences = extract_sentences(normalized_tokens)
        checked_sentences = []
        for sent in sentences:
            checked_sentences.extend(tts_frontend.tts_spellcheck(sent).split())

        #print("NORMALIZED: " + str(normalized_tokens))
        #print("SPELLCHECKED: " + str(checked_sentences))
        spellchecked_normalized = []
        for token in normalized_tokens:
            if isinstance(token, TagToken):
                spellchecked_normalized.append(token)
            elif checked_sentences[0] == token.name:
                spellchecked_normalized.append(token)
                checked_sentences = checked_sentences[1:]
            else:
                spellchecked = checked_sentences[:len(token.name.split())]
                token.set_normalized(' '.join(spellchecked))
                spellchecked_normalized.append(token)
                checked_sentences = checked_sentences[len(token.name.split()):]

        #print("NORMALIZED_SPELLCHECKED: " + str(spellchecked_normalized))
        return spellchecked_normalized
