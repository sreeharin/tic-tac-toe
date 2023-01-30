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

    def test_invalid_input(self):
        self.protocol.lineReceived(b'test')
        res = {"response": "invalid input"}
        self.assertEqual(self.tr.value(), dumps(res).encode('utf-8') + b'\r\n')

    def test_invalid_game_code(self):
        join = {"action": "JOIN", "data": {"game_code": "test"}}
        self.protocol.lineReceived(dumps(join).encode('utf-8'))
        res = {"response": "invalid game_code"}
        self.assertEqual(self.tr.value(), dumps(res).encode('utf-8') + b'\r\n')

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
        join = {"action": "JOIN", "data": {"game_code": game_code}}
        self.tr.clear()
        self.protocol.lineReceived(dumps(join).encode('utf-8'))
        res = {"response": "joined room"}
        self.assertEqual(self.tr.value(), dumps(res).encode('utf-8') + b'\r\n')
        self.assertEqual(len(self.factory.game_rooms[game_code].players), 2)

    def test_cancel_game(self):
        raise Exception("Not implemented")

    def test_eval(self):
        raise Exception("Not implemented")

