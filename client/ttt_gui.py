#!/usr/bin/env python

'''
Author: shn
License: MIT License
'''

import sys
import json
from tkinter import Tk, Frame, Label, Button, Entry, StringVar
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor, tksupport
from twisted.python import log

sys.path.append('../')
from server.response import Response

log.startLogging(sys.stdout)
CURRENT_FRAME = None
BTNS_STATE = None


class TicTacToeClientProtocol(LineReceiver):
    def connectionMade(self):
        print('Connection established with server')
        self.factory.client = self

    def connectionLost(self, reason):
        pass

    def lineReceived(self, line):
        line = line.decode('utf-8')
        self.factory.handle_line(line)


class TicTacToeClientFactory(ClientFactory):
    protocol = TicTacToeClientProtocol

    def __init__(self):
        self.client = None

    def handle_line(self, line: str) -> None:
        '''Reads response from line and does appropriate task'''
        json_data = json.loads(line)
        response = json_data.get('RES')

        match response:
            case Response.ROOM_CREATED:
                game_code = json_data.get('GAME_CODE')
                print(f'Game room created with code: {game_code}')
                switch_frame(CURRENT_FRAME, 'WaitingFrame', game_code)
            case Response.CANCELLED_ROOM:
                print('Room cancelled')
                switch_frame(CURRENT_FRAME, 'MainFrame')
            case Response.JOINED_ROOM:
                print('Joined ROOM')
            case Response.GAME_CODE_NOT_FOUND:
                print('Game code not found')
            case Response.GAME_STRING_NOT_FOUND:
                print('Game string not found')
            case Response.INVALID_INPUT:
                print('Invalid input')
            case Response.INVALID_DATA:
                print('Invalid data')
            case Response.INVALID_GAME_CODE:
                print('Invalid game code')
            case Response.ROOM_FULL:
                print('Room full')
            case Response.NOT_AUTHORIZED:
                print('Not authorized')
            case Response.UNKNOWN_ACTION:
                print('Unknown action')
            case Response.UNKNOWN_ERROR:
                print('Unknown error')

    def host_game(self) -> None:
        print('Hosting game')
        host_data = {
                "action": "HOST",
                "data": None,
                }
        if self.client is not None:
            self.client.sendLine(json.dumps(host_data).encode('utf-8'))
        else:
            print('Can\'t host game. Not connected to server.')

    def join_game(self, game_code: str) -> None:
        print(f'Joining game with game code: {game_code}')
        join_data = {
                "action": "JOIN",
                "data": {
                    "game_code": game_code
                    }
                }
        if self.client is not None:
            self.client.sendLine(json.dumps(join_data).encode('utf-8'))
        else:
            print('Can\'t join game room. Not connected to server.')

    def cancel_game_room(self, game_code: str) -> None:
        print(f'Cancelling game room with code: {game_code}')
        cancel_data = {
                "action": "CANCEL",
                "data": {
                    "game_code": game_code,
                    }
                }
        if self.client is not None:
            self.client.sendLine(json.dumps(cancel_data).encode('utf-8'))
        else:
            print('Can\'t cancel game room. Not connected to server')

    def eval_btn_click(self, btn_no: int) -> None:
        print(f"Clicked btn: {btn_no}")
        if BTNS_STATE[btn_no].get() == "":
            BTNS_STATE[btn_no].set("X")
            game_string = ''.join(
                    btn.get()
                    if btn.get() != "" else "-" for btn in BTNS_STATE)
            print(game_string)


def switch_frame(current_frame: any, new_frame: str,
                 game_code: str = None) -> None:
    '''Switches between frames'''
    global CURRENT_FRAME
    match new_frame:
        case 'MainFrame':
            tmpFrame = MainFrame(current_frame.master, current_frame.factory)
            tmpFrame.pack()
            CURRENT_FRAME = tmpFrame
        case 'JoinFrame':
            tmpFrame = JoinFrame(current_frame.master, current_frame.factory)
            tmpFrame.pack()
            CURRENT_FRAME = tmpFrame
        case 'WaitingFrame':
            tmpFrame = WaitingFrame(current_frame.master,
                                    current_frame.factory, game_code)
            tmpFrame.pack()
            CURRENT_FRAME = tmpFrame
        case _:
            print('Unknown frame')
            reactor.stop()
    current_frame.destroy()


class MainFrame(Frame):
    '''First frame which is shown when the GUI is run'''
    def __init__(self, master, factory):
        self.master = master
        self.factory = factory
        super().__init__(self.master)
        self.pack()
        self.__create_widgets()

    def __create_widgets(self):
        labelFrame = Frame(self)
        label1 = Label(
                labelFrame, text="Tic Tac Toe",
                pady=5, font=(20),
                )
        label2 = Label(
                labelFrame, text="Play tic tac toe with your friends",
                padx=10
                )

        btnFrame = Frame(self)
        btn1 = Button(
                btnFrame, text="Host",
                command=lambda: self.factory.host_game()
                )
        btn2 = Button(
                btnFrame, text="Join",
                command=lambda: switch_frame(self, 'JoinFrame')
                )

        labelFrame.grid(row=0, column=0)
        label1.grid(row=0, column=0)
        label2.grid(row=1, column=0)

        btnFrame.grid(row=1, column=0)
        btn1.grid(row=0, column=0, padx=5, pady=10)
        btn2.grid(row=0, column=1, padx=5, pady=10)


class JoinFrame(Frame):
    '''Frame for joining game using game code'''
    def __init__(self, master, factory):
        self.master = master
        self.factory = factory
        super().__init__(self.master)
        self.pack()
        self.__create_widgets()

    def __create_widgets(self):
        frame1 = Frame(self)
        label1 = Label(
                frame1, text="Join game room",
                pady=5, font=(20)
                )
        label2 = Label(
                frame1, text="Enter the game code to play with your friend",
                padx=10
                )
        game_code = Entry(frame1)
        frame1.grid(row=0, column=0)
        label1.grid(row=0, column=0)
        label2.grid(row=1, column=0)
        game_code.grid(row=2, column=0, pady=5)

        frame2 = Frame(self)
        btn1 = Button(
                frame2, text="Go back",
                command=lambda: switch_frame(self, 'MainFrame')
                )
        btn2 = Button(
                frame2, text="Join room",
                command=lambda: self.factory.join_game(game_code.get())
                )

        frame2.grid(row=1, column=0)
        btn1.grid(row=0, column=0, padx=5, pady=10)
        btn2.grid(row=0, column=1, padx=5, pady=10)


class WaitingFrame(Frame):
    def __init__(self, master, factory, game_code):
        self.master = master
        self.factory = factory
        self.game_code = game_code
        super().__init__(self.master)
        self.pack()
        self.__create_widgets()

    def __create_widgets(self):
        frame1 = Frame(self)
        label0 = Label(frame1, text="Game hosted", font=(24))
        label1 = Label(frame1, text=f"Your game code is {self.game_code}")
        label2 = Label(frame1, text="Share with your friend to let them join",
                       padx=10)
        label3 = Label(
                frame1, text="Waiting for your friend to join the game...",
                padx=15, pady=5)

        frame1.grid(row=0, column=0)
        label0.grid(row=0, column=0)
        label1.grid(row=1, column=0)
        label2.grid(row=2, column=0)
        label3.grid(row=3, column=0)

        frame2 = Frame(self)
        btn1 = Button(frame2, text="Cancel game room",
                      command=lambda: self.factory.cancel_game_room(
                          self.game_code)
                      )
        frame2.grid(row=1, column=0)
        btn1.grid(row=0, column=0, pady=10)


class GameFrame(Frame):
    def __init__(self, master, factory):
        self.master = master
        self.factory = factory
        super().__init__(self.master)
        self.pack()
        self.__create_widgets()

    def __create_widgets(self):
        global BTNS_STATE
        frame1 = Frame(self)
        label1 = Label(frame1, text="You're playing with your friend")

        frame1.grid(row=0, column=0)
        label1.grid(row=0, column=0, padx=10, pady=5)

        frame2 = Frame(self, bg="black")
        frame2.grid(row=1, column=0, pady=10)

        btns = [
                Button(frame2, height=2, width=3,
                       textvariable=BTNS_STATE[no],
                       command=lambda idx=no: self.factory.eval_btn_click(idx),
                       ) for no in range(9)
                ]
        row = 0
        col = 0
        for idx, btn in enumerate(btns):
            if (idx) % 3 == 0:
                row += 1
                col = 0
            btn.grid(row=row, column=col, padx=1, pady=1)
            col += 1


if __name__ == '__main__':
    try:
        assert len(sys.argv) >= 3
    except AssertionError:
        print(f'example usage: {sys.argv[0]} host port')
        sys.exit(-1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    factory = TicTacToeClientFactory()

    root = Tk()
    root.title("Tic Tac Toe")
    root.protocol("WM_DELETE_WINDOW", lambda: reactor.stop())

    tksupport.install(root)
    # CURRENT_FRAME = MainFrame(root, factory)
    BTNS_STATE = [StringVar() for _ in range(9)]
    CURRENT_FRAME = GameFrame(root, factory)
    reactor.connectTCP(host, port, factory)
    reactor.run()
