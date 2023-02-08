class Room:
    def __init__(self, game_code: str = None,
                 players: list = [], x: int = None,
                 o: int = None, game_string: str = None):
        '''Room class'''
        self.game_code = game_code
        self.players = players
        self.x = x
        self.o = o
        self.game_string = game_string
