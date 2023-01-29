import sys
from twisted.trial import unittest
from twisted.test import proto_helpers
from json import dumps

sys.path.append('../')
from ttt_server import TicTacToeProtocol

class TestServer(unittest.TestCase):
    def setUp(self):
        self.protocol = TicTacToeProtocol() 
        self.tr = proto_helpers.StringTransport()
        self.protocol.makeConnection(self.tr)

    def test_host_game(self):
        data = {
            'cmd': 'host'    
        }

        data_ok = {
            'res': 'ok'
        }
        self.protocol.lineReceived(dumps(data).encode('utf-8'))
        self.assertEqual(self.tr.value(), dumps(data_ok).encode('utf-8'))

    def test_join_game(self):
        raise Exception("Not implemented")

    def test_cancel_game(self):
        raise Exception("Not implemented")
