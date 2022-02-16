from .tokens import Token


def init_tokens(text: str) -> list:
    tokens_list = []
    running_char_ind = 0
    for tok in text.split(' '):
        base_token = Token(tok)
        base_token.set_index(len(tokens_list))
        base_token.set_span(running_char_ind, running_char_ind + len(tok))
        running_char_ind += len(tok) + 1 #count for space after current token
        tokens_list.append(base_token)

    return tokens_list


def extract_text(token_list: list) -> str:
    token_strings = []
    for elem in token_list:
        token_strings.append(elem.name)
    return ' '.join(token_strings)
