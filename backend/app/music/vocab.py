from collections import Counter

def build_vocab(token_lists):
    counter = Counter()

    for tokens in token_lists:
        counter.update(tokens)

    vocab = {token: idx for idx, token in enumerate(counter)}
    return vocab
