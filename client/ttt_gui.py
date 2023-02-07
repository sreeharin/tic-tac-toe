#!/usr/bin/env python

'''
Author: shn
License: MIT License
'''

import sys
import json
from tkinter import Tk, Frame, Label, Button, Entry
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor, tksupport

CURRENT_FRAME = None

class TicTacToeClientProtocol(LineReceiver):
    def connectionMade(self):
        print('Connection Made To Server')
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
        json_data = json.loads(line) 
        response = json_data.get('response')

        match response:
            case 'room created':
                game_code = json_data.get('game_code')
                switch_frame(CURRENT_FRAME, 'WaitingFrame', game_code)
            case _:
                print('Hmm')

    def host_game(self) -> None:
        print('Hosting game')
        host_data = {
                "action": "HOST",
                "data": None,
                }
        if self.client != None:
            self.client.sendLine(json.dumps(host_data).encode('utf-8'))
            print('host game command send')
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
        if self.client != None:
            self.client.sendLine(json.dumps(join_data).encode('utf-8'))
        else:
            print('Can\'t join game room. Not connected to server.')

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
        label1 = Label(frame1, text=f"Your game code is {self.game_code}")
        label2 = Label(frame1, text="Share with your friend to let them join")

        frame1.grid(row=0, column=0)
        label1.grid(row=0, column=0)
        label2.grid(row=1, column=0)

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
    CURRENT_FRAME = MainFrame(root, factory)
    reactor.connectTCP(host, port, factory)
    reactor.run()

