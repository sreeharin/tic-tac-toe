#!/usr/bin/env python

'''
Author: shn
License: MIT License
'''

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
        if self.client != None:
            self.client.sendLine(json.dumps(host_data).encode('utf-8'))
            print('host game command send')
        else:
            print('Not connected to server')

class MainWindow(Frame):
    '''First window which is shown when the GUI is run'''
    def __init__(self, master, factory):
        super().__init__(master)
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
            command=lambda: factory.host_game()
        )
        btn2 = Button(btnFrame, text="Join")

        labelFrame.grid(row=0, column=0)
        label1.grid(row=0, column=0)
        label2.grid(row=1, column=0)

        btnFrame.grid(row=1, column=0)
        btn1.grid(row=0, column=0, padx=5, pady=10)
        btn2.grid(row=0, column=1, padx=5, pady=10)

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

