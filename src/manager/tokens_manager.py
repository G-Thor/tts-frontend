import logging
import re
from .tokens import Token, TagToken, CleanToken, NormalizedToken


def init_tokens(text: str) -> list:
    tokens_list = []
    running_char_ind = 0
    for tok in text.split(' '):
        if not tok:
            continue
        base_token = Token(tok.strip())
        base_token.set_index(len(tokens_list))
        base_token.set_span(running_char_ind, running_char_ind + len(tok))
        running_char_ind += len(tok) + 1 #count for space after current token
        tokens_list.append(base_token)

    return tokens_list


def extract_text(token_list: list, ignore_tags=True, word_separator='') -> str:
    token_strings = []
    for elem in token_list:
        if isinstance(elem, TagToken) and ignore_tags:
            continue
        if not elem.name:
            continue
        token_strings.append(elem.name)
    if word_separator:
        return f' {word_separator} '.join(token_strings)
    else:
        return ' '.join(token_strings)


def extract_tagged_text(token_list: list, ignore_tags=True) -> str:
    token_strings = []
    for elem in token_list:
        if isinstance(elem, TagToken) and ignore_tags:
            continue
        if not isinstance(elem, NormalizedToken):
            ValueError('We can only extract tagged text from NormalizedTokens, not from ' + str(type(elem)))
        token_strings.append(elem.name)
        token_strings.append(' ')
        token_strings.append(elem.pos)
        if elem.pos == '.':
            token_strings.append('\n')
        else:
            token_strings.append(' ')
    return ' '.join(token_strings).strip()


def extract_tokenized_text(sentences: list) -> str:
    """
    Extract the string from the list of sentences: [[],[], ..., []]
    :param sentences: list of strings
    :return: a string representation of 'sentences'
    """
    tokenized_text = ''
    for sent in sentences:
        tokenized_text += ' ' + sent

    return tokenized_text.strip()


def align_tokens(clean_token_list: list, tokenized: list) -> list:
    """Compare token_list to the tokenized string and adjust tokens list if they differ.
    We compare length of token_list to the length of tokenized.split(). If they differ in length
    we compare them tokenwise, and also compare the tokens by length.
    This alignment is necessary since the cleaning is done before the tokenizing.

    :param clean_token_list: a tokenList containing cleaned tokens, but not necessarily correctly tokenized
    :param tokenized: a tokenized version of the tokenList as a list of sentences, tokens separated by a space
    :return a list of cleanTokens, possibly a longer one than the original"""

    clean_str = extract_text(clean_token_list)
    tokenized_string = extract_tokenized_text(tokenized)
    # make sure we are merging token lists created from the same string
    # remove white spaces, since the tokenizer might have added some
    pattern = re.compile(r'\s+')
    if re.sub(pattern, '', clean_str) != re.sub(pattern, '', tokenized_string):
        logging.error(clean_str + ' and ' + tokenized_string + ' are not the same, can not merge token lists!')
        raise ValueError('params do not represent the same original string!')

    token_list = tokenized_string.split()
    aligned_list = []
    j = 0
    for i, token in enumerate(clean_token_list):
        if token.name == token_list[j]:
            aligned_list.append(token)
        else:
            clean_token = CleanToken(token.get_original_token())
            clean_token.set_clean(token_list[j])
            aligned_list.append(clean_token)
            non_splitted_token = token_list[j]
            while non_splitted_token != token.name and j < len(token_list) - 2:
                j += 1
                clean_token = CleanToken(token.get_original_token())
                clean_token.set_clean(token_list[j])
                aligned_list.append(clean_token)
                non_splitted_token += token_list[j]
        j += 1

    return aligned_list
