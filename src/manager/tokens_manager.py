import logging
import re
from .tokens import Token, TagToken, CleanToken, NormalizedToken
from .settings import SENTENCE_TAG

def init_tokens(text: str) -> list:
    tokens_list = []
    running_char_ind = 0
    for tok in text.split():
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


def extract_sentences(token_list: list, ignore_tags=True, word_separator='') -> list:
    """Return a list of sentences as represented in token_list. Even if ignore_tags is set to
    True we check for sentence tags to split the list into sentences."""
    sentences = []
    sent_tokens = []
    for elem in token_list:
        if isinstance(elem, TagToken) and elem.name == SENTENCE_TAG:
            if word_separator:
                sent = f' {word_separator} '.join(sent_tokens)
            else:
                sent = ' '.join(sent_tokens)
            sentences.append(sent)
            sent_tokens = []
        elif isinstance(elem, TagToken) and ignore_tags:
            continue
        elif not elem.name:
            continue
        else:
            sent_tokens.append(elem.name)

    if sent_tokens:
        if word_separator:
            sent = f' {word_separator} '.join(sent_tokens)
        else:
            sent = ' '.join(sent_tokens)
        sentences.append(sent)

    return sentences


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


def extract_tokenized_text(sentences: list, sent_split=False) -> str:
    """
    Extract the string from the list of sentences: [[],[], ..., []]
    :param sentences: list of strings
    :return: a string representation of 'sentences'
    """
    tokenized_text = ''
    for sent in sentences:
        if sent_split:
            # replace full stop with sentence-tag
            if sent.endswith('.'):
                sent = sent[:-1]
            tokenized_text += ' ' + sent + ' ' +SENTENCE_TAG
        else:
            tokenized_text += ' ' + sent

    return re.sub('\s+', ' ', tokenized_text).strip()


def align_tokens(clean_token_list: list, tokenized: list, split_sent: bool=False) -> list:
    """Compare token_list to the tokenized string and adjust tokens list if they differ.
    We compare length of token_list to the length of tokenized.split(). If they differ in length
    we compare them tokenwise, and also compare the tokens by length.
    This alignment is necessary since the cleaning is done before the tokenizing.

    :param clean_token_list: a tokenList containing cleaned tokens, but not necessarily correctly tokenized
    :param tokenized: a tokenized version of the tokenList as a list of sentences, tokens separated by a space
    :return a list of cleanTokens, possibly a longer one than the original"""

    clean_str = extract_text(clean_token_list)
    tokenized_string = extract_tokenized_text(tokenized, sent_split=split_sent)
    # make sure we are merging token lists created from the same string
    # remove white spaces and sentence tags, since the tokenizer might have added spaces and the tokenized
    # string might already containe sentence tags
    tmp_tokenized = tokenized_string.replace(SENTENCE_TAG, '.')
    pattern = re.compile(r'[\s.]+')
    if re.sub(pattern, '', clean_str) != re.sub(pattern, '', tmp_tokenized):
        logging.error(clean_str + ' and ' + tokenized_string + ' are not the same, can not merge token lists!')
        raise ValueError('params do not represent the same original string!')

    token_list = tokenized_string.split()
    aligned_list = []
    i = 0
    j = 0
    # if the token_list containes tags, we need to step back in the enumeration of the clean_token_list
    set_step_back_counter = False
    while i < len(clean_token_list):
        if i == 1275:
            print('check')
        if set_step_back_counter:
            i -= 1
            set_step_back_counter = False
        token = clean_token_list[i]
        if j >= len(token_list):
            print('j: ' + str(j) + ', i: ' + str(i) + ' ' + token.name)
        elif token.name == token_list[j]:
            aligned_list.append(token)
        elif isinstance(token, TagToken):
            aligned_list.append(token)
            # tag tokens are not present in token_list, halt the counting for token_list
            j -= 1
        elif token_list[j].startswith('<'):
            tag_token = TagToken(token_list[j], j)
            aligned_list.append(tag_token)
            set_step_back_counter = True
        else:
            clean_token = CleanToken(token.get_original_token())
            clean_token.set_clean(token_list[j])
            aligned_list.append(clean_token)
            non_splitted_token = token_list[j]
            while non_splitted_token != re.sub(pattern, '', token.name) and j < len(token_list) - 2:
                j += 1
                if token_list[j].startswith('<'):
                    j -= 1
                    break
                clean_token = CleanToken(token.get_original_token())
                clean_token.set_clean(token_list[j])
                aligned_list.append(clean_token)
                non_splitted_token += token_list[j]
        i += 1
        j += 1
    # last closing tag in token_list?
    if j < len(token_list) and token_list[j].startswith('<'):
        tag_token = TagToken(token_list[j], j)
        aligned_list.append(tag_token)

    return aligned_list
