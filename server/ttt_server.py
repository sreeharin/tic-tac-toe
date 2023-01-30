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
    # def connectionMade(self):
    #     addr = self.transport.getPeer()
    #     logging.info('A new connection is established: %s' % (addr.host))

    def lineReceived(self, line):
        try:
            line = line.decode('utf-8')
            json_data = json.loads(line)
            self.handle_line(json_data)
        except json.decoder.JSONDecodeError:
            self.write_response('invalid input')

    def handle_line(self, json_data):
        action = json_data.get('action', None)
        data = json_data.get('data', None)

        if action == 'HOST':
            logging.info(
                'New game room created by : %s' % self.transport.getPeer()
            )
            gc = game_code()
            self.factory.game_rooms[gc] = Room(
                game_code = gc, players = [self.transport.getPeer()]
            )
            self.write_response('room created') 

        elif action == 'JOIN':
            if data == None:
                self.write_response('invalid data')
                return

            gc = data.get('game_code', None) 
            if gc == None:
                self.write_response('game_code not found')
                return

            if gc not in self.factory.game_rooms:
                self.write_response('invalid game_code')
                return

            self.factory.game_rooms[gc].players.append(
                self.transport.getPeer()
            )
            self.write_response('joined room')
        elif action == 'CANCEL':
            pass
        else:
            pass

    def write_response(self, msg: str) -> None:
        res = {'response': msg}
        self.sendLine(json.dumps(res).encode('utf-8'))

class TicTacToeFactory(protocol.ServerFactory):
    protocol = TicTacToeProtocol

    def __init__(self):
        self.game_rooms = {} 

if __name__ == '__main__':
    logging.info('Starting Tic Tac Toe server')
    ttt_end_point = endpoints.serverFromString(reactor, "tcp:8081")
    ttt_end_point.listen(TicTacToeFactory())
    reactor.run()
