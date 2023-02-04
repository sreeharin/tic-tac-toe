import sys
from tkinter import Frame, Entry, Button, Label

sys.path.append('../')
# from actions import join_window_actions as actions
import actions.switch_frame as sf

class JoinWindow(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        label1 = Label(
            self, text = "Enter the game code", 
            font=(16))
        entry1 = Entry(self)
        btn1 = Button(self, text = "Enter room")
        btn2 = Button(
            self, text = "Go back", 
            command = lambda: sf.switch_frame(self, 'MainWindow') 
        )

        label1.grid(row=0, column=0, pady=5, columnspan=2)
        entry1.grid(row=1, column=0, padx="10", pady=10, columnspan=2)
        btn2.grid(row=2, column=0, padx="10", pady=10)
        btn1.grid(row=2, column=1, padx="10", pady=10)
