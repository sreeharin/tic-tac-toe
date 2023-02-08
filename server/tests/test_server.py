from twisted.trial import unittest
from twisted.test import proto_helpers
from json import dumps
import sys

sys.path.append('../')
from ttt_server import TicTacToeFactory
from response import Response

class TestServer(unittest.TestCase):
    def setUp(self):
        self.factory = TicTacToeFactory()
        self.protocol = self.factory.buildProtocol(['127.0.0.1', 0])
        self.tr = proto_helpers.StringTransport()
        self.protocol.makeConnection(self.tr)

    def test_invalid_input(self):
        '''Tests if the input is invalid or not'''
        self.protocol.lineReceived(b'test')
        res = {"RES": Response.INVALID_INPUT}
        self.assertEqual(self.tr.value(), dumps(res).encode('utf-8') + b'\r\n')

    def test_invalid_game_code(self):
        '''Tests if given game code exists'''
        join = {"action": "JOIN", "data": {"game_code": "test"}}
        cancel = {"action": "CANCEL", "data": {"game_code": "test"}}
        eval_game = {
            "action": "EVAL", 
            "data": {
                "game_code": "test",
                "game_string": "test"
                }
            }
        res = {"RES": Response.INVALID_GAME_CODE}
        self.protocol.lineReceived(dumps(join).encode('utf-8'))
        self.assertEqual(self.tr.value(), dumps(res).encode('utf-8') + b'\r\n')
        self.tr.clear()
        self.protocol.lineReceived(dumps(cancel).encode('utf-8'))
        self.assertEqual(self.tr.value(), dumps(res).encode('utf-8') + b'\r\n')
        self.tr.clear()
        self.protocol.lineReceived(dumps(eval_game).encode('utf-8'))
        self.assertEqual(self.tr.value(), dumps(res).encode('utf-8') + b'\r\n')

    def test_game_string_not_found(self):
        '''Tests if game_string is in request'''
        host = {"action": "HOST", "data": None}
        self.protocol.lineReceived(dumps(host).encode('utf-8'))
        game_code = list(self.factory.game_rooms.keys())[0]
        self.tr.clear()
        eval_game = {
            "action": "EVAL", 
            "data": {
                "game_code": game_code,
            }
        }
        self.protocol.lineReceived(dumps(eval_game).encode('utf-8'))
        res = {"RES": Response.GAME_STRING_NOT_FOUND}
        self.assertEqual(self.tr.value(), dumps(res).encode('utf-8') + b'\r\n')

    def test_cancel_game_room_without_authorization(self):
        '''Tests if a game can be cancelled without being in the room'''
        host = {"action": "HOST", "data": None}
        self.protocol.lineReceived(dumps(host).encode('utf-8'))
        game_code = list(self.factory.game_rooms.keys())[0]
        self.tr.clear()
        self.assertEqual(len(self.factory.game_rooms), 1)
        self.assertIn(game_code, self.factory.game_rooms)
        self.factory.game_rooms[game_code].players = []
        cancel = {"action": "CANCEL", "data": {"game_code": game_code}}
        self.protocol.lineReceived(dumps(cancel).encode('utf-8'))
        res = {"RES": Response.NOT_AUTHORIZED}
        self.assertEqual(self.tr.value(), dumps(res).encode('utf-8') + b'\r\n')

    def test_join_full_room(self):
        '''Tests if a player can join an ongoing game with two players'''
        host = {"action": "HOST", "data": None}
        self.protocol.lineReceived(dumps(host).encode('utf-8'))
        game_code = list(self.factory.game_rooms.keys())[0]
        self.tr.clear()
        join = {"action": "JOIN", "data": {"game_code": game_code}}
        self.protocol.lineReceived(dumps(join).encode('utf-8'))
        self.assertEqual(len(self.factory.game_rooms[game_code].players), 2)
        self.tr.clear()
        self.protocol.lineReceived(dumps(join).encode('utf-8'))
        res = {"RES": Response.ROOM_FULL}
        self.assertEqual(self.tr.value(), dumps(res).encode('utf-8') + b'\r\n')

    def test_host_game(self):
        '''Tests game hosting'''
        tmp = {"action": "HOST", "data": None}
        self.assertEqual(len(self.factory.game_rooms), 0)
        self.protocol.lineReceived(dumps(tmp).encode('utf-8'))
        self.assertEqual(len(self.factory.game_rooms), 1)

    def test_join_game(self):
        '''Tests game joining'''
        host = {"action": "HOST", "data": None}
        self.protocol.lineReceived(dumps(host).encode('utf-8'))
        game_code = list(self.factory.game_rooms.keys())[0]
        self.tr.clear()
        join = {"action": "JOIN", "data": {"game_code": game_code}}
        self.protocol.lineReceived(dumps(join).encode('utf-8'))
        self.assertEqual(len(self.factory.game_rooms[game_code].players), 2)

    def test_cancel_game_room(self):
        '''Tests game cancelling'''
        host = {"action": "HOST", "data": None}
        self.protocol.lineReceived(dumps(host).encode('utf-8'))
        game_code = list(self.factory.game_rooms.keys())[0]
        self.tr.clear()
        self.assertEqual(len(self.factory.game_rooms), 1)
        self.assertIn(game_code, self.factory.game_rooms)
        cancel = {"action": "CANCEL", "data": {"game_code": game_code}}
        self.protocol.lineReceived(dumps(cancel).encode('utf-8'))
        res = {"RES": Response.CANCELLED_ROOM}
        self.assertEqual(self.tr.value(), dumps(res).encode('utf-8') + b'\r\n')
        self.assertNotIn(game_code, self.factory.game_rooms)

    def test_eval(self):
        '''Tests game string evaluation'''
        host = {"action": "HOST", "data": None}
        self.protocol.lineReceived(dumps(host).encode('utf-8'))
        game_code = list(self.factory.game_rooms.keys())[0]
        self.tr.clear()
        eval_game = {
            "action": "EVAL", 
            "data": {
                "game_code": game_code,
                "game_string": "oxoxo-oxx"
            }
        }
        self.protocol.lineReceived(dumps(eval_game).encode('utf-8'))
        res = {"RES": "o_won"}
        self.assertEqual(self.tr.value(), dumps(res).encode('utf-8') + b'\r\n')

    def test_find_game_code(self):
        '''Test for finding game_code from address'''
        tmp = {"action": "HOST", "data": None}
        self.assertEqual(len(self.factory.game_rooms), 0)
        self.protocol.lineReceived(dumps(tmp).encode('utf-8'))
        game_code = list(self.factory.game_rooms.keys())[0]
        self.assertEqual(len(self.factory.game_rooms), 1)
        addr = self.tr.getPeer()
        self.assertEqual(self.factory.find_game_code(addr), game_code)

    def test_player_mark_assignments(self):
        '''Test if players are assigned x and o randomly after joining'''
        host_data = {"action": "HOST", "data": None}   
        self.protocol.lineReceived(dumps(host_data).encode('utf-8'))
        game_code = list(self.factory.game_rooms.keys())[0]
        self.tr.clear()
        join_data = {"action": "JOIN", "data": {"game_code": game_code}}
        self.protocol.lineReceived(dumps(join_data).encode('utf-8'))
        self.assertEqual(len(self.factory.game_rooms[game_code].players), 2)
        self.assertFalse(
                self.factory.game_rooms[game_code].x 
                is self.factory.game_rooms[game_code].o)

