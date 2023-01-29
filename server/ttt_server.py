from twisted.internet import protocol, reactor, endpoints
from twisted.protocols import basic
from twisted.application import service
import logging
import json

logging.basicConfig(
    filename='ttt-server.log', encoding='utf-8', 
    format="%(asctime)s [%(levelname)s]: %(message)s", level=logging.DEBUG
)

class TicTacToeProtocol(basic.LineReceiver):
    def connectionMade(self):
        addr = self.transport.getPeer()
        logging.info('A new connection is established: %s' % (addr.host))

    # def connectionLost(self):
    #     pass

    def lineReceived(self, line):
        line = line.decode('utf-8')
        res = None
        try:
            json_data = json.loads(line)
            res = json_data 
        except json.decoder.JSONDecodeError:
            res = {
                'msg': 'error'
            }
        
        self.transport.write(json.dumps(res).encode('utf-8'))
        self.transport.loseConnection()

class TicTacToeFactory(protocol.ServerFactory):
    protocol = TicTacToeProtocol

    def __init__(self):
        pass

if __name__ == '__main__':
    logging.info('Starting Tic Tac Toe server')
    ttt_end_point = endpoints.serverFromString(reactor, "tcp:8081")
    ttt_end_point.listen(TicTacToeFactory())
    reactor.run()
