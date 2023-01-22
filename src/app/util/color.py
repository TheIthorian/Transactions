import random


def rand_color(seed: str = "color"):
    random.seed(seed)
    r = lambda: random.randint(0, 255)

    return "#%02X%02X%02X" % (r(), r(), r())
