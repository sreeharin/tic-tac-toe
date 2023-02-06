#!/usr/bin/env python

import sys
import json
from tkinter import Tk, Frame, Label, Button
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor, tksupport

class TicTacToeClientProtocol(LineReceiver):
    def connectionMade(self):
        print('Connection Made To Server')
        self.factory.client = self

    def connectionLost(self, reason):
        pass

    def lineReceived(self, line):
        print(line)


class TicTacToeClientFactory(ClientFactory):
    protocol = TicTacToeClientProtocol

    def __init__(self):
        self.client = None

    def host_game(self):
        host_data = {
            "action": "HOST",
            "data": None,
        }
        self.client.sendLine(json.dumps(host_data).encode('utf-8'))
        print('host game command send')

class MainWindow(Frame):
    def __init__(self, master, factory):
        super().__init__(master)
        self.pack()
        self.__create_widgets()

    def __create_widgets(self):
        label1 = Label(self, text="Tic Tac Toe")
        label2 = Label(self, text="Play tic tac toe with your friends")
        btn1 = Button(
            self, text="Host", command=lambda: factory.host_game()
        )

        label1.pack()
        label2.pack()
        btn1.pack()

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
    MainWindow(root, factory)
    reactor.connectTCP(host, port, factory)
    reactor.run()

