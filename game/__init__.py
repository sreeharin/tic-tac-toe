#!/usr/bin/env python

'''
Author: shn
License: MIT License
'''

'''
0 1 2
3 4 5
6 7 8
'''

def convert(game_string: str) -> dict:
    '''Convert game string into game map'''
    game_map = {
        'h': [
            game_string[:3],
            game_string[3:6],
            game_string[6:]
        ],
        'v': [
            game_string[::3],
            game_string[1::3],
            game_string[2::3],
        ],
        'd': [
            game_string[::4],
            game_string[2::2][:-1]
        ],
    }
    return game_map

def draw(game_string: str) -> bool:
    '''Check if game is draw'''
    return False

def x_wins(game_string: str) -> bool:
    '''Check if x won the game'''
    return False

def o_wins(game_string: str) -> bool:
    '''Check if o won the game'''
    return False
