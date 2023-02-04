import sys
sys.path.append('../')

def switch_frame(current_frame: any, frame_name: str) -> None:
    '''Switch frames'''
    if frame_name == 'JoinWindow':
        from frames.join_window import JoinWindow
        frame = JoinWindow()
        current_frame.destroy()
        frame.tkraise() 
    elif frame_name == 'MainWindow':
        from frames.main_window import MainWindow
        frame = MainWindow()
        current_frame.destroy()
        frame.tkraise()
    else:
        #Log to file
        print(f"Frame not found: {frame_name}")
