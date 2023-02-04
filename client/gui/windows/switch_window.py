def switch_window(current_window: any, window_name: str) -> None:
    '''Switch windows'''
    if window_name == 'JoinWindow':
        from .join_window import JoinWindow
        window = JoinWindow()
        current_window.destroy()
        window.tkraise() 
    elif window_name == 'MainWindow':
        from .main_window import MainWindow
        window = MainWindow()
        current_window.destroy()
        window.tkraise()
    else:
        #Log to file
        print(f"Frame not found: {window_name}")
