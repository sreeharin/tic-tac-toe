import sys
sys.path.append('../')
from frames.join_window import JoinWindow

def host():
    print('Host')
    
def join(self):
    '''Switch from MainWindow to JoinWindow'''
    self.pack_forget()
    JoinWindow().pack()
