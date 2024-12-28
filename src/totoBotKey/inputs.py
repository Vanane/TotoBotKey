"""Input controller
Intercept input events and manages user events trigger and execution
"""
import traceback
from concurrent.futures import Future, ThreadPoolExecutor
from multiprocessing.managers import SharedMemoryManager
from typing import Callable, Tuple, List, Dict
from evdevUtils import getDevices, listener, enums
from evdev import InputDevice
from . import keys

class Event:
    binding:Tuple[int]
    function:Callable
    exactMatch:bool

    def __init__(self, b, f, e):
        self.binding = b
        self.function = f
        self.exactMatch = e


events: Dict[Tuple[int], Event]

keyStates: int

eventFutures: List[Future]
eventsPool: ThreadPoolExecutor
sharedMem: SharedMemoryManager

ydotoold: InputDevice


def init():
    global keyStates, events, eventFutures, eventsPool, sharedMem, ydotoold

    keyStates = 0
    events = dict()

    eventsPool = ThreadPoolExecutor(max_workers=10)

    ydotoold = getDevices(lambda d: d.name == "ydotoold virtual device")

def getBindFromKeys(keys:list):
    """Returns a bitfield representing a binding of keycodes. The bits at the slots of each keycode's code is equal to 1"""
    r = 0
    for k in keys:
        r |= (1<<k)
    return r


def addEvent(bind:list, f: Callable, exclusively:bool = True):
    """Adds an user-defined event to the manager.

    Args:
        keys (str): combination of keycodes that should trigger the function
        f (_type_): function to call in reaction to this event
    """
    events[int(not exclusively)|(getBindFromKeys(bind)<<1)] = Event(bind, f, True)
    print(f"Event Any '{bind}' added")


def isPressed(key:int | list):
    """Return the state of a given keycode"""
    return keyStates & getBindFromKeys(key if key is list else [key])


def pressed(data) -> bool:
    """Updates the keyStates state to whichever key has just been pressed"""
    global keyStates
    keyStates = keyStates|(1<<data.code)

def released(data) -> bool:
    """Updates the keyStates state to whichever key has just been released"""
    global keyStates
    keyStates = keyStates&~(1<<data.code)

def checkUserEvents(bind: int, curKeysBind: int) -> bool:
    """Tries to find and call user events with the given binding."""
    state = False
    try:
        bind = bind<<1
        curKeysBind = curKeysBind<<1

        if e := events.get(0|bind, False):
            f = eventsPool.submit(eventThread, e.function)
            print(f"Event '{e.binding}' called successfully through Future {str(f)}")
            state = True


        for e in list(filter(lambda e: (1|bind)&e == e and 1&e == 1 and curKeysBind&e == curKeysBind, events)):
            f = eventsPool.submit(eventThread, events[e].function)
            print(f"Event '{events[e].binding}' called successfully through Future {str(f)}")
            state = True

    except Exception:
        traceback.print_exc()
        state = False

    return state


def eventThread(event: Callable):
    """Event thread"""
    try:
        event()
    except Exception:
        traceback.print_exc()

def playback(data):
    """Plays an event on ydotoold device"""
    ydotoold.write(data.type, data.code, data.value)
    ydotoold.write(enums.EV_SYN, 0, 0) # Writing a SYN event to make sure that the playback effect is immediate. Delay happens otherwise.

def callback(data):
    """Callback that's called by DevEvent whener any input events occurs on any devices.
    It will manage keys states, and event triggering when necessary

    Args:
        data (tuple): Event data, as defined in the Linux [Userspace API](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/include/uapi/linux/input.h)
    """
    global ydotoold
    # Excluding mouse clicks and mouse movements from macros, for soft lock reasons
    if data.code in [272, 273] or data.type in [enums.EV_ABS, enums.EV_REL]:
        return playback(data)

    # Has an event been fired with this data ?
    # If not, then the input event should be exploitable by the system.
    event = False
    match int(data.type):
        case enums.EV_KEY:
            if data.code == 1 and data.value == 0 and isPressed(29): # if Ctrl+Esc
                listener.running = False
                playback(data) # Playing back the "Esc release" event
                datb = data
                datb.code = 29
                playback(datb) # Playing a "Ctrl release" event, just in case the timing makes it wrong
                return
            match data.value:
                case 1:
                    pressed(data)
                    event = checkUserEvents(keyStates, getBindFromKeys([data.code]))
                case 0:
                    released(data)
                case _:
                    pass
        case _:
            pass

    if not event:
        playback(data)


def cleanUp():
    """Cleans thread pool up"""
    print("Shutting down inputs thread pool...")
    for k in keys.keysDict:
        ydotoold.write(enums.EV_KEY, keys.keysDict[k], 0)
    ydotoold.write(enums.EV_SYN, 0, 0)
    eventsPool.shutdown()
