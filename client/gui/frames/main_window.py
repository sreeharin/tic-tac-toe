from tkinter import Frame, Label, Button

class MainWindow(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
       
    def create_widgets(self):
        textFrame = Frame(self, width = 350, height = 70)
        textFrame.grid(row=0, column=0)
        label1 = Label(textFrame, text = "Tic Tac Toe", font=(24))
        label2 = Label(textFrame, text = "Play tic tac toe with your friends", padx=10)

        label1.grid(row=0, column=0, pady=5)
        label2.grid(row=1, column=0)

        btnsFrame = Frame(self, width = 350, height = 100)
        btnsFrame.grid(row=1, column=0)

        btn1 = Button(btnsFrame, text = "Host")
        btn2 = Button(btnsFrame, text = "Join")

        btn1.grid(row=0, column=0, padx=20, pady=25)
        btn2.grid(row=0, column=1, padx=20, pady=25)




        
