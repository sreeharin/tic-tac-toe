'''
Author: shn
License: MIT License
'''

import secrets
import string

def game_code(n: int = 5) -> str:
    return ''.join(secrets.choice(string.ascii_letters) for _ in range(n))
