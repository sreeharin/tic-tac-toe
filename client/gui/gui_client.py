from tkinter import Tk
from frames.main_window import MainWindow
# from frames.join_window import JoinWindow

if __name__ == '__main__':
    root = Tk()
    root.title("Tic Tac Toe")
    # root.geometry("350x200")
    # root.maxsize(width=350, height=200)
    # root.minsize(width=350, height=200)
    app = MainWindow(root)
    app.mainloop()
