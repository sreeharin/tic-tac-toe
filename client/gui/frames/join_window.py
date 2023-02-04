from tkinter import Frame, Entry, Button, Label

class JoinWindow(Frame):
    def __init__(self, master=None):
        master.geometry("350x150")
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        joinFrame = Frame(self, height = 100, width = 350)
        joinFrame.grid()

        label1 = Label(
            joinFrame, text = "Enter the game code", 
            font=(16))
        entry1 = Entry(joinFrame)
        btn1 = Button(joinFrame, text = "Enter room")

        label1.grid(row=0, column=0, pady=5)
        entry1.grid(row=1, column=0, padx="10", pady=10)
        btn1.grid(row=1, column=1, padx="10", pady=10)

