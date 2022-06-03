from typing import Dict, Set, Union
from string import ascii_uppercase, hexdigits

import random

def hashIDFromString(string: str):
    # fast hashing
    random.seed(string)
    h = random.getrandbits(128)
    return "%032x" % h
