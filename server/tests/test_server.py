import sys
from twisted.trial import unittest
from twisted.test import proto_helpers
from json import dumps

sys.path.append('../')
from ttt_server import TicTacToeProtocol, TicTacToeFactory

class TestServer(unittest.TestCase):
    def setUp(self):
        # self.protocol = TicTacToeProtocol() 
        self.factory = TicTacToeFactory()
        self.protocol = self.factory.buildProtocol(['127.0.0.1', 0])
        self.tr = proto_helpers.StringTransport()
        self.protocol.makeConnection(self.tr)

    def test_host_game(self):
        tmp = {
            "action": "HOST"
        }
        res = {
            "response": "room created"
        }
        self.protocol.lineReceived(dumps(tmp).encode('utf-8'))
        self.assertEqual(self.tr.value(), dumps(res).encode('utf-8') + b'\r\n')
        self.assertEqual(len(self.factory.game_rooms), 1)

    def test_join_game(self):
        raise Exception("Not implemented")

    def test_cancel_game(self):
        raise Exception("Not implemented")
