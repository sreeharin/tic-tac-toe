from twisted.trial import unittest
from twisted.test import proto_helpers
from json import dumps
import sys

sys.path.append('../')
from ttt_server import TicTacToeFactory

class TestServer(unittest.TestCase):
    def setUp(self):
        self.factory = TicTacToeFactory()
        self.protocol = self.factory.buildProtocol(['127.0.0.1', 0])
        self.tr = proto_helpers.StringTransport()
        self.protocol.makeConnection(self.tr)

    #SAD PATHS

    def test_invalid_input(self):
        self.protocol.lineReceived(b'test')
        res = {"response": "invalid input"}
        self.assertEqual(self.tr.value(), dumps(res).encode('utf-8') + b'\r\n')

    def test_invalid_game_code(self):
        join = {"action": "JOIN", "data": {"game_code": "test"}}
        cancel = {"action": "CANCEL", "data": {"game_code": "test"}}
        res = {"response": "invalid game_code"}
        self.protocol.lineReceived(dumps(join).encode('utf-8'))
        self.assertEqual(self.tr.value(), dumps(res).encode('utf-8') + b'\r\n')
        self.tr.clear()
        self.protocol.lineReceived(dumps(cancel).encode('utf-8'))
        self.assertEqual(self.tr.value(), dumps(res).encode('utf-8') + b'\r\n')

    def test_cancel_game_room_without_authorization(self):
        '''Trying to cancel a game room without being in it'''
        host = {"action": "HOST", "data": None}
        self.protocol.lineReceived(dumps(host).encode('utf-8'))
        game_code = list(self.factory.game_rooms.keys())[0]
        self.tr.clear()
        self.assertEqual(len(self.factory.game_rooms), 1)
        self.assertIn(game_code, self.factory.game_rooms)
        self.factory.game_rooms[game_code].players = []
        cancel = {"action": "CANCEL", "data": {"game_code": game_code}}
        self.protocol.lineReceived(dumps(cancel).encode('utf-8'))
        res = {"response": "not authorized to cancel game room"}
        self.assertEqual(self.tr.value(), dumps(res).encode('utf-8') + b'\r\n')

    #HAPPY PATHS

    def test_host_game(self):
        tmp = {"action": "HOST", "data": None}
        res = {"response": "room created"}
        self.assertEqual(len(self.factory.game_rooms), 0)
        self.protocol.lineReceived(dumps(tmp).encode('utf-8'))
        self.assertEqual(self.tr.value(), dumps(res).encode('utf-8') + b'\r\n')
        self.assertEqual(len(self.factory.game_rooms), 1)

    def test_join_game(self):
        host = {"action": "HOST", "data": None}
        self.protocol.lineReceived(dumps(host).encode('utf-8'))
        game_code = list(self.factory.game_rooms.keys())[0]
        self.tr.clear()
        join = {"action": "JOIN", "data": {"game_code": game_code}}
        self.protocol.lineReceived(dumps(join).encode('utf-8'))
        res = {"response": "joined room"}
        self.assertEqual(self.tr.value(), dumps(res).encode('utf-8') + b'\r\n')
        self.assertEqual(len(self.factory.game_rooms[game_code].players), 2)

    def test_cancel_game_room(self):
        host = {"action": "HOST", "data": None}
        self.protocol.lineReceived(dumps(host).encode('utf-8'))
        game_code = list(self.factory.game_rooms.keys())[0]
        self.tr.clear()
        self.assertEqual(len(self.factory.game_rooms), 1)
        self.assertIn(game_code, self.factory.game_rooms)
        cancel = {"action": "CANCEL", "data": {"game_code": game_code}}
        self.protocol.lineReceived(dumps(cancel).encode('utf-8'))
        res = {"response": "cancelled game room"}
        self.assertEqual(self.tr.value(), dumps(res).encode('utf-8') + b'\r\n')
        # self.assertEqual(len(self.factory.game_rooms), 0)
        self.assertNotIn(game_code, self.factory.game_rooms)

    def test_eval(self):
        raise Exception("Not implemented")

