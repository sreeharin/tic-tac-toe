'''
Author: shn
License: MIT License
'''

import logging
import json
from twisted.internet import protocol, reactor, endpoints
from twisted.protocols import basic
from twisted.application import service
from ipaddress import IPv4Address
from tools.game_code import game_code
from models.room import Room
from game.ttt import eval_game
from response import Response

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
        logging.info(
                f'Connection lost by {addr.host} [{reason.getErrorMessage()}]'
                )
    
        gc = self.factory.find_game_code(addr) 
        if gc:
            try:
                if self.factory.game_rooms[gc].players[0] == self.transport:
                    del self.factory.game_rooms[gc]
                    logging.info(f'Deleted room with game_code: {gc}')
                else:
                    self.factory.game_rooms[gc].players.pop()
            except KeyError:
                pass

    def lineReceived(self, line):
        try:
            line = line.decode('utf-8')
            json_data = json.loads(line)
            self.handle_line(json_data)
        except json.decoder.JSONDecodeError:
            self.write_response(Response.INVALID_INPUT)
        # except Exception as e:
        #     logging.error(
        #             f'Unknown error {e} occured while parsing: {line}'
        #             )
        #     self.write_response(Response.UNKNOWN_ERROR)

    def handle_line(self, json_data):
        action = json_data.get('action', None)
        data = json_data.get('data', None)

        if action == 'HOST':
            gc = game_code()
            addr = self.transport.getPeer()
            logging.info(
                    f'New game room created by {addr.host} with game_code: {gc}' 
                    )
            self.factory.game_rooms[gc] = Room(
                    game_code = gc, players = [self.transport]
                    )
            res = {
                    "RES": Response.ROOM_CREATED,
                    "GAME_CODE": gc,
                    }
            self.sendLine(json.dumps(res).encode('utf-8'))

        elif action == 'JOIN':
            if not data:
                self.write_response(Response.INVALID_DATA)
                return

            gc = data.get('game_code', None) 
            if not gc:
                self.write_response(Response.GAME_CODE_NOT_FOUND)
                return

            if not self.factory.valid_game_code(gc):
                self.write_response(Response.INVALID_GAME_CODE)
                return
            
            if len(self.factory.game_rooms[gc].players) < 2:
                logging.info(f'New player joining game room: {gc}')
                self.factory.game_rooms[gc].players.append(self.transport)
                # self.write_response(Response.JOINED_ROOM)
                res = {"RES": Response.JOINED_ROOM}
                for player in self.factory.game_rooms[gc].players:
                    player.write(json.dumps(res).encode('utf-8') + b'\r\n')
            else:
                self.write_response(Response.ROOM_FULL)

        elif action == 'CANCEL':
            gc = data.get('game_code', None) 
            if not self.factory.valid_game_code(gc):
                self.write_response(Response.INVALID_GAME_CODE)
                return

            addr = self.transport.getPeer() 
            if addr not in [player.getPeer() for player in self.factory.game_rooms[gc].players]:
                self.write_response(Response.NOT_AUTHORIZED)
                return

            try:
                logging.info(f'Player cancelling game room: {gc}')
                del self.factory.game_rooms[gc]
                self.write_response(Response.CANCELLED_ROOM)
                return
            except Exception as e:
                logging.error(
                    f'Unknown error occured while trying to cancel game: {e}'
                )
                self.write_reponse(Response.UNKNOWN_ERROR) 

        elif action == 'EVAL':
            game_string = data.get('game_string', None)
            gc = data.get('game_code', None)
            if not game_string:
                self.write_response(Response.GAME_STRING_NOT_FOUND)
                return
            if not gc:
                self.write_response(Response.GAME_CODE_NOT_FOUND)
                return
            if not self.factory.valid_game_code(gc):
                self.write_response(Response.INVALID_GAME_CODE)
                return

            logging.info('Player evaluating game string')
            for player in self.factory.game_rooms[gc].players:
                res = {"RES": eval_game(game_string)}
                player.write(json.dumps(res).encode('utf-8') + b'\r\n')

        else:
            logging.error(f'Unknown action: {action}')
            self.write_response(Response.UNKNOWN_ACTION)

    def write_response(self, msg: str) -> None:
        '''Sends reponse back to other end'''
        res = {'RES': msg}
        self.sendLine(json.dumps(res).encode('utf-8'))

class TicTacToeFactory(protocol.ServerFactory):
    protocol = TicTacToeProtocol

    def __init__(self):
        self.game_rooms = {} 

    def valid_game_code(self, game_code: str) -> bool:
        '''Checks if game code is valid or not'''
        return True if game_code in self.game_rooms else False

    def find_game_code(self, addr: IPv4Address) -> str:
        '''Returns game code from player's address''' 
        game_rooms = [*self.game_rooms.values()]
        tmp = list(filter(
            lambda x: addr in [player.getPeer() for player in x.players], 
            game_rooms
        ))
        try:
            return tmp[0].game_code
        except IndexError:
            return None

if __name__ == '__main__':
    logging.info('Starting Tic Tac Toe server')
    ttt_end_point = endpoints.serverFromString(reactor, "tcp:8081")
    ttt_end_point.listen(TicTacToeFactory())
    reactor.run()
