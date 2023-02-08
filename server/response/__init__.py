from enum import IntFlag, auto

class Response(IntFlag):
    '''Responses sent by server'''
    ROOM_CREATED = auto() 
    CANCELLED_ROOM = auto() 
    JOINED_ROOM = auto() 
    GAME_STRING_EVAL = auto()
    GAME_CODE_NOT_FOUND = auto() 
    GAME_STRING_NOT_FOUND = auto() 
    INVALID_INPUT = auto()
    INVALID_DATA = auto()
    INVALID_GAME_CODE = auto() 
    ROOM_FULL = auto() 
    NOT_AUTHORIZED = auto() 
    UNKNOWN_ACTION = auto() 
    UNKNOWN_ERROR = auto()
