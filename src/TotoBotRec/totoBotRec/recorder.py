import time
from typing import Callable
from enum import Enum
import traceback

from evdev import InputEvent
from evdevUtils import enums as evs
import evdevUtils.listener as listener
from totoBotKey.inputs import getBindFromKeys


class RecordType(Enum):
    """"""
    WAIT = 0
    CLICK = 1
    MOUSEMOVE = 2
    KEY = 3

class KeyType(Enum):
    """"""    
    UP = 0
    DOWN = 1


class Record():
    """"""
    type_: RecordType

    args: list
    """Contains details corresponding to type_ :
    - WAIT :        0 => delay

    - CLICK :       0 => int : button
                    1 => (int, int) : position

    - MOUSEMOVE :   0 => (int, int) : start position
                    1 => (int, int) : end position

    - KEY :         0 => int : keycode
                    1 => KeyType : key status
    """

    def __init__(self, type_:RecordType, args:list):
        """.ctor"""
        self.type_ = type_
        self.args = args

    def __str__(self):
        match self.type_:
            case RecordType.WAIT:
                return f"Wait {self.args[0]} ms"
            case RecordType.CLICK:
                return f"Click button {self.args[0]} at coordinates {self.args[1]}"
            case RecordType.MOUSEMOVE:
                return f"Move cursor from coordinates {self.args[0]} to coordinates {self.args[1]}"
            case RecordType.KEY:
                return f"Press key {self.args[0]} {KeyType(self.args[1]).name}"
            case _:
                return f"Do whatever {str(self.args)} means"
        return ""


records: list[Record]

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

_killswitch:int

def getRecords():
    global records

    return records

def record(considerWait:bool = False, considerCursor:bool = False, waitThreshold:int = 0):
    """Starts recording any events that occurs on any keyboard and mouse devices
    
    Args:
        considerWait (bool): If True, inactive periods will be recorded as well (see `waitThreshold`).
        considerCursor (bool): If True, the cursor path will be recorded as well. Else, only the cursor coordinates will be recorded, when succeeded by another event.
        waitThreshold (int): If greater than 0 and `considerWait` is True, only inactive periods greater than `waitThreshold` ms will be recorded, and they will be recorded as multiples of `waitThreshold`."""
    global _waitHandler, _cursorHandler, _considerWait, _considerCursor, _waitThreshold, _keyHandler, _lastEvent, _lastTime, _killswitch
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
    _killswitch = 0

    _lastEvent = InputEvent(-1, -1, -1, -1, -1)
    _lastTime = time.time_ns()

    listener.listen(False)

    handleExit()


def _getCursorPos():
    return (0,0)

def _handleInput(data:InputEvent):
    """"""
    if not listener.running:
        return
    try:
        # If mouse move, ignore. Mouse movements are handled when the position changed compared to the previous event
        global _lastTime, _lastEvent, _waitHandler, _cursorHandler, _keyHandler, _killswitch

        _killswitchHandler(data)

        _waitHandler(data)

        match data.type:
            case evs.EV_KEY:
                _keyHandler(data)
            case evs.EV_REL | evs.EV_ABS:
                _handleCursorMove(data)
                pass

        _lastEvent = data
        _lastTime = time.time_ns() / 1000000
    except Exception:
        traceback.print_exc()
        state = False



def _handleWait(data:InputEvent):
    """"""
    global _waitThreshold, _lastTime
    global records

    w = time.time_ns() / 1000000 - _lastTime
    if _waitThreshold > 0:
        w = w - (w % _waitThreshold)
    if w > 0:
        records.append(Record(RecordType.WAIT, [w]))


def _discardWait(data:InputEvent):
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
    global _mouseKeys
    global records

    records.append(Record(RecordType.CLICK, [data.code, _getCursorPos()]))


def _handleKey(data:InputEvent):
    """"""
    global _mouseKeys
    global records

    if data.type == evs.EV_KEY and data.value in[0, 1]:
        if data.code in _mouseKeys:
            records.append(Record(RecordType.CLICK, [data.code, _getCursorPos()]))
        else:
            records.append(Record(RecordType.KEY, [data.code, data.value]))


def _killswitchHandler(data:InputEvent):
    global _killswitch

    if data.type == evs.EV_KEY and data.code in[1, 29]:
        _killswitch = _killswitch|(1<<data.code) if data.value == 1 else _killswitch&~(1<<data.code)

    if _killswitch == getBindFromKeys([1, 29]):
        listener.running = False
        return


def handleExit():
    global records
    listener.cleanUp()
    try:
        for i in range(len(records), 0, step = -1):
            if records[i - 1].args[0] in [1, 29] and records[i - 2].args[0] in [1, 29]:
                records.pop(i - 1)
                records.pop(i - 2)
                break
            i -= 1
    except Exception:
        pass
