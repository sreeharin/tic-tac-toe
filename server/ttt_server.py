from twisted.internet import protocol, reactor, endpoints
from twisted.protocols import basic
from twisted.application import service
import logging
import json
from tools.game_code import game_code
from models.room import Room

logging.basicConfig(
    filename='ttt-server.log', encoding='utf-8', 
    format="%(asctime)s [%(levelname)s]: %(message)s", level=logging.DEBUG
)

class TicTacToeProtocol(basic.LineReceiver):
    def connectionMade(self):
        addr = self.transport.getPeer()
        logging.info('A new connection is established: %s' % (addr.host))

    def lineReceived(self, line):
        res = None
        try:
            line = line.decode('utf-8')
            json_data = json.loads(line)
            self.handle_line(json_data)
        except json.decoder.JSONDecodeError:
            res = {
                'response': 'Invalid input'
            }
            self.transport.write(json.dumps(res).encode('utf-8'))

    def handle_line(self, json_data):
        action = json_data['action']
        # data = json_data['data']

        if action == 'HOST':
            gc = game_code()
            self.factory.game_rooms.append(Room(
                game_code = gc, players = [self.transport.getPeer()]
                ))
            self.write_response('room created') 
        elif action == 'JOIN':
            pass
        elif action == 'EVAL':
            pass
        else:
            pass

    def write_response(self, msg: str) -> None:
        res = {
            'response': msg
        }
        self.sendLine(json.dumps(res).encode('utf-8'))

class TicTacToeFactory(protocol.ServerFactory):
    protocol = TicTacToeProtocol

    def __init__(self):
        self.game_rooms = []

if __name__ == '__main__':
    logging.info('Starting Tic Tac Toe server')
    ttt_end_point = endpoints.serverFromString(reactor, "tcp:8081")
    ttt_end_point.listen(TicTacToeFactory())
    reactor.run()
