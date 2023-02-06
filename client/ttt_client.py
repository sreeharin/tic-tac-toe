import json
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

class TicTacToeClientProtocol(LineReceiver):
    def connectionMade(self):
        pass

    def connectionLost(self, reason):
        pass

    def lineReceived(self, line):
        self.writeLine(line)

    def host_room(self):
        host_room = {
            "action": "HOST",
            "data": None
        }
        self.writeLine(json.dumps(host_room).encode('utf-8'))

class TicTacToeClientFactory(ClientFactory):
    def buildProtocol(self, addr):
        return TicTacToeClientProtocol()

# if __name__ == '__main__':
#     reactor.connectTCP('127.0.0.1', 8081, TicTacToeClientFactory())
#     reactor.run()
