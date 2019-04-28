from random import Random


CHARACTERS = "abcdefghijklmnopqrstuvwxyz0123456789"


choose = Random().choice


def random_token() -> str:
    return ''.join(choose(CHARACTERS) for dummy in range(8))
