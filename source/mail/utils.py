from random import randint, shuffle


def generate_verification_code() -> str:
    vocab = [chr(randint(65, 90)) for _ in range(5)]
    vocab += [chr(randint(48, 57)) for _ in range(5)]
    shuffle(vocab)

    return ''.join(vocab[:5])
