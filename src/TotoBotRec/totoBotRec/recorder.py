import evdevUtils.listener as listener
from evdevUtils import enums as evs
from evdev import InputEvent
import time
from typing import Callable
from enum import Enum

class RecordType(Enum):
    """"""
    WAIT = 0
    CLICK = 1,
    MOUSEMOVE = 2,
    KEY = 3

class KeyType(Enum):
    """"""
    DOWN = 1,
    UP = 0

class Record():
    """"""
    type_: RecordType
    args: list

    def __init__(self, type_:RecordType, args:list):
        """.ctor"""
        self.type_ = type_
        self.args = args


records: list[InputEvent]

_considerWait:bool
_considerCursor:bool

_lastEvent:InputEvent
_lastTime:int
_waitThreshold:int

_waitHandler:Callable[int, int]
_cursorHandler:Callable
_keyHandler:Callable

_cursorStart:(int, int)

_mouseKeys = [i for i in range(272, 277)]


def record(considerWait:bool = False, considerCursor:bool = False, waitThreshold:int = 0):
    """Starts recording any events that occurs on any keyboard and mouse devices
    
    Args:
        considerWait (bool): If True, inactive periods will be recorded as well (see `waitThreshold`).
        considerCursor (bool): If True, the cursor path will be recorded as well. Else, only the cursor coordinates will be recorded, when succeeded by another event.
        waitThreshold (int): If greater than 0 and `considerWait` is True, only inactive periods greater than `waitThreshold` ms will be recorded, and they will be recorded as multiples of `waitThreshold`."""
    global _waitHandler, _cursorHandler, _considerWait, _considerCursor, _waitThreshold, _keyHandler, _lastEvent
    global records

    listener.init()
    listener.subscribeToAll(_handleInput)

    _considerWait = considerWait
    _considerCursor = considerCursor
    _waitThreshold = waitThreshold

    _waitHandler = _handleWait if _considerWait else _discardWait
    _cursorHandler = _handleCursorMove if _considerCursor else _handleCursor

    _keyHandler = _handleKey

    records = list()

    _lastEvent = InputEvent(-1, -1, -1, -1, -1)

    listener.listen(False)


def _getCursorPos():
    return (0,0)

def _handleInput(data:InputEvent):
    """"""
    # If mouse move, ignore. Mouse movements are handled when the position changed compared to the previous event
    global _lastTime, _lastEvent, _waitHandler, _cursorHandler, _keyHandler

    _waitHandler(_lastTime, time.time_ns())

    match data.type:
        case evs.EV_KEY:
            _keyHandler(data)
        case evs.EV_ABS | evs.EV_REL:
            _cursorHandler(data)
        case _:
            pass

    _lastEvent = data
    _lastTime = time.time_ns()
    pass


def _handleWait(last:int, new:int):
    """"""
    global _waitThreshold
    global records

    w = new - last
    if _waitThreshold > 0:
        w = w - (w % _waitThreshold)

    records.append(Record(RecordType.WAIT, w))

def _discardWait(last:int, new:int):
    """"""
    pass

def _handleCursorMove(data:InputEvent):
    """"""
    global _lastEvent, _cursorStart, _mouseKeys
    global records

    match _lastEvent.type:
        case evs.EV_ABS | evs.EV_REL:
            if data.type == evs.EV_KEY:
                # Last event was mousemove, new event isn't, so mouse movement stopped
                # Adding record as a line from cursorStart up to current cursor position
                records.append(Record(RecordType.MOUSEMOVE, [_cursorStart, _getCursorPos()]))
                if data.code in _mouseKeys:
                    records.append(Record(RecordType.CLICK, [data.code, _getCursorPos()]))
                return
        case evs.EV_KEY:
            if data.type in [evs.EV_ABS, evs.EV_REL]:
                # Last event isn't a mousemove, new event is, so mouse movement started
                ## Setting _cursorStart to current cursor position
                _cursorStart = _getCursorPos()


def _handleCursor(data:InputEvent):
    """"""
    global _mouseKeys, _cursorStart
    global records

    records.append(Record(RecordType.CLICK, [data.code, _getCursorPos()]))


def _handleKey(data:InputEvent):
    """"""
    global _lastEvent, _cursorHandler
    global records

    if data.code in _mouseKeys:
        _cursorHandler(data)
    else:
        records.append(Record(RecordType.KEY, [data.code, data.value]))
