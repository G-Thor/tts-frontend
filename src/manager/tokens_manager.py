from .tokens import Token, TagToken, NormalizedToken


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


def extract_text(token_list: list, ignore_tags=True) -> str:
    token_strings = []
    for elem in token_list:
        if isinstance(elem, TagToken) and ignore_tags:
            continue
        if not elem.name:
            continue
        token_strings.append(elem.name)
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
