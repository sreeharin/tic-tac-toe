'''
Author: shn
License: MIT License
'''

from twisted.internet import protocol, reactor, endpoints
from twisted.protocols import basic
from twisted.application import service
import logging
import json
from tools.game_code import game_code
from models.room import Room
from game.ttt import eval_game

logging.basicConfig(
    filename='ttt-server.log', encoding='utf-8', 
    format="%(asctime)s [%(levelname)s]: %(message)s", level=logging.DEBUG
)

class TicTacToeProtocol(basic.LineReceiver):
    def connectionMade(self):
        addr = self.transport.getPeer()
        logging.info('A new connection is established: %s' % (addr.host))

    def connectionLost(self, reason):
        addr = self.transport.getPeer()
        logging.info(f'Connection lost by {addr.host} due to {reason}')

    def lineReceived(self, line):
        try:
            line = line.decode('utf-8')
            json_data = json.loads(line)
            self.handle_line(json_data)
        except json.decoder.JSONDecodeError:
            self.write_response('invalid input')
        except Exception as e:
            logging.error(
                f'Unknown error {e} occured while parsing: {line}'
            )
            self.write_response('unknown error occured')

    def handle_line(self, json_data):
        action = json_data.get('action', None)
        data = json_data.get('data', None)

        if action == 'HOST':
            logging.info(
                'New game room created by : %s' % self.transport.getPeer().host
            )
            gc = game_code()
            self.factory.game_rooms[gc] = Room(
                game_code = gc, players = [self.transport]
            )
            self.write_response('room created') 

        elif action == 'JOIN':
            logging.info(
                'New player joining game room'
            )
            if not data:
                self.write_response('invalid data')
                return

            gc = data.get('game_code', None) 
            if not gc:
                self.write_response('game_code not found')
                return

            if not self.factory.valid_game_code(gc):
                self.write_response('invalid game_code')
                return
            
            if len(self.factory.game_rooms[gc].players) < 2:
                self.factory.game_rooms[gc].players.append(self.transport)
                self.write_response('joined room')
            else:
                self.write_response('room full')

        elif action == 'CANCEL':
            logging.info('Player cancelling game room')
            gc = data.get('game_code', None) 
            if not self.factory.valid_game_code(gc):
                self.write_response('invalid game_code')
                return

            addr = self.transport.getPeer() 
            if addr not in [player.getPeer() for player in self.factory.game_rooms[gc].players]:
                self.write_response('not authorized to cancel game room')
                return

            try:
                del self.factory.game_rooms[gc]
                self.write_response('cancelled game room')
                return
            except Exception as e:
                logging.error(
                    f'Unknown error occured while trying to cancel game: {e}'
                )
                self.write_reponse('unknown error occured') 

        elif action == 'EVAL':
            game_string = data.get('game_string', None)
            gc = data.get('game_code', None)
            if not game_string:
                self.write_response('game_string not found')
                return
            if not gc:
                self.write_response('game_code not found')
                return
            if not self.factory.valid_game_code(gc):
                self.write_response('invalid game_code')
                return

            for player in self.factory.game_rooms[gc].players:
                res = {
                    "response": eval_game(game_string)
                }
                player.write(json.dumps(res).encode('utf-8') + b'\r\n')

        else:
            logging.error(f'Unknown action: {action}')
            self.write_response('unknown action')

    def write_response(self, msg: str) -> None:
        '''Sends reponse back to other end'''
        res = {'response': msg}
        self.sendLine(json.dumps(res).encode('utf-8'))

class TicTacToeFactory(protocol.ServerFactory):
    protocol = TicTacToeProtocol

    def __init__(self):
        self.game_rooms = {} 

    def valid_game_code(self, game_code: str) -> bool:
        '''Checks if game code is valid or not'''
        return True if game_code in self.game_rooms else False

if __name__ == '__main__':
    logging.info('Starting Tic Tac Toe server')
    ttt_end_point = endpoints.serverFromString(reactor, "tcp:8081")
    ttt_end_point.listen(TicTacToeFactory())
    reactor.run()
