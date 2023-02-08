#!/usr/bin/env python

'''
Author: shn
License: MIT License
'''

from enum import StrEnum, auto

class Result(StrEnum):
    DRAW = auto()
    X_WON = auto()
    O_WON = auto()
    ONGOING = auto()

def convert(game_string: str) -> dict:
    '''Convert game string into game map'''
    game_string = game_string.lower()
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
    if (not x_wins(game_string) and \
        not o_wins(game_string) and \
        '-' not in game_string):
        return True
    return False

def x_wins(game_string: str) -> bool:
    '''Check if x won the game'''
    game_map = convert(game_string)
    if 3*'x' in game_map['h']+game_map['v']+game_map['d']:
        return True
    return False

def o_wins(game_string: str) -> bool:
    '''Check if o won the game'''
    game_map = convert(game_string)
    if 3*'o' in game_map['h']+game_map['v']+game_map['d']:
        return True
    return False

def eval_game(game_string: str) -> Result:
    '''Evaluates the status of the game'''
    if draw(game_string):
        return Result.DRAW
    else:
        if x_wins(game_string):
            return Result.X_WON
        elif o_wins(game_string):
            return Result.O_WON
        else:
            return Result.ONGOING
