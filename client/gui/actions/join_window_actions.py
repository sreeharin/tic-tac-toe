import sys
sys.path.append('../')

def go_back(self):
    '''Switch from JoinWindow to MainWindow'''
    from frames.main_window import MainWindow
    self.pack_forget()
    MainWindow().pack()
