#!/usr/bin/env python

'''
Tests for game package

Author: shn
License: MIT License
'''

import unittest
import sys

sys.path.append('../')
from game.ttt import convert, draw, x_wins, o_wins, eval_game, Result

class TestGame(unittest.TestCase):
    def test_convert(self):
        '''Test if game string is converted to game map'''
        test_string = '012345678'
        game_map = convert(test_string)
        
        self.assertEqual(game_map['h'], ['012', '345', '678'])
        self.assertEqual(game_map['v'], ['036', '147', '258'])
        self.assertEqual(game_map['d'], ['048', '246'])

    def test_draw(self):
        '''Test if game is a draw'''
        draw_game1 = 'xoxooxoxo'
        draw_game2 = 'xoooxxxoo'
        draw_game3 = 'xoooxxoxo'
        win_game1 = 'ooxoxxxoo'
    
        self.assertTrue(draw(draw_game1))
        self.assertTrue(draw(draw_game2))
        self.assertTrue(draw(draw_game3))
        self.assertFalse(draw(win_game1))

    def test_x_wins(self):
        '''Test if x won the game'''
        x_win_game1 = 'xooxxooox'
        x_win_game2 = 'x--x--x--'
        x_win_game3 = 'oxoxxx-oo'
        x_lose_game1 = 'oxxoxooox'

        self.assertTrue(x_wins(x_win_game1))
        self.assertTrue(x_wins(x_win_game2))
        self.assertTrue(x_wins(x_win_game3))
        self.assertFalse(x_wins(x_lose_game1))

    def test_o_wins(self):
        '''Test if o won the game'''
        o_win_game1 = 'oxoxoxxoo'
        o_win_game2 = 'x-o-oxox-'
        o_win_game3 = 'x-xooo-x-'
        o_lose_game1 = 'xxxooxo--'

        self.assertTrue(o_wins(o_win_game1))
        self.assertTrue(o_wins(o_win_game2))
        self.assertTrue(o_wins(o_win_game3))
        self.assertFalse(o_wins(o_lose_game1))

    def test_eval_game(self):
        '''Tests for eval_game'''
        o_win_game = 'oxoxoxxoo'
        x_win_game = 'xooxxooox'
        draw_game = 'xoxooxoxo'
        ongoing_game = 'x--------'

        self.assertEqual(eval_game(o_win_game), Result.O_WON)
        self.assertEqual(eval_game(x_win_game), Result.X_WON)
        self.assertEqual(eval_game(draw_game),  Result.DRAW)
        self.assertEqual(eval_game(ongoing_game), Result.ONGOING)

