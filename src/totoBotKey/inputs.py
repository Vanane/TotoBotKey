"""input
"""

from concurrent.futures import Future, ThreadPoolExecutor
from multiprocessing.managers import SharedMemoryManager
from typing import Callable, List, Dict
from evdevUtils import getDevices, listener, enums
from evdev import InputDevice
from . import runtime
import os
import signal
import regex



EV = "EVENTS"


eventsOnAny: dict
eventsOnOnly:dict

keyStates: dict

eventFutures: List[Future]
eventsPool: ThreadPoolExecutor
sharedMem: SharedMemoryManager

ydotoold: InputDevice


def init():
    global keyStates, eventsOnAny, eventsOnOnly, eventFutures, eventsPool, sharedMem, ydotoold

    keyStates = dict()
    eventsOnAny = dict()
    eventsOnOnly = dict()

    eventsPool = ThreadPoolExecutor(max_workers=10)

    ydotoold = getDevices(lambda d: d.name == "ydotoold virtual device")


def keyPressed(data) -> bool:
    """The given keycode is flagged as currently held down in the keyPresses dict.
    Called whenever an input event is caught, and the "value" field equals 1.
    """
    keyStates[data.code] = True
    return callEvent()


def keyReleased(data) -> bool:
    """The given keycode is removed from the keyPresses dict.
    Called whenever an input event is caught, and the "value" field equals 0.
    """
    keyStates.pop(data.code, None)
    return False


def callEvent(ev: str = None) -> bool:
    """Tries to find and call a given user event, not generating any error in the absence of one."""
    state = False
    try:
        if ev is None:
            return callEvent("+".join(sorted(map(str, keyStates))))

        print(f"Trying to call event '{ev}'")
        if eventsOnOnly.get(ev, False):
            f = eventsPool.submit(eventThread, eventsOnAny[ev])
            print(f"Event '{ev}' called successfully through Future {str(f)}")
            state = True

        keys = eventsOnAny.keys()
        for k in keyStates:
            keys = list(filter(lambda e: regex.match(f"(?:^|\+)({k})(?:$|\+)", e), keys))
        
        for k in keys:
            f = eventsPool.submit(eventThread, eventsOnAny[ev])
            print(f"Event '{ev}' called successfully through Future {str(f)}")
            state = True
        
        
    except Exception as e:
        print(e)
        state = False
    
    return state


def eventThread(event: Callable):
    try:
        event()
    except Exception as e:
        print(e)


def isPressed(key):
    """Return the state of a given keycode"""
    return keyStates.get(int(key), False)


def addEventOnAny(comb: str, f: Callable):
    """Adds an user-defined event to the manager.

    Args:
        comb (str): combination of keycodes that should trigger the function,
        in this format : xx+yy+zz
        f (_type_): function to call in reaction to this event
    """
    eventsOnAny[comb] = f
    print(f"Event '{comb}' added")

def addEventOnOnly(comb: str, f: Callable):
    eventsOnOnly[comb] = f
    print(f"Event '{comb}' added")

def devEventCallback(data):
    """Callback that's called by DevEvent whener any input events occurs on any devices.
    It will manage keys states, and event triggering when necessary

    Args:
        data (tuple): Event data, as defined in the Linux [Userspace API](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/include/uapi/linux/input.h)
    """
    global ydotoold

    if data.code in [272, 273]:
        return playback(data)

    # Has an event been fired with this data ?
    # If not, then the input event should be exploitable by the system.
    event = False

    match int(data.type):
        case enums.EV_KEY:
            if data.value == 0 and data.code == 1:
                #return os.kill(os.getpid(), signal.SIGINT)
                listener.running = False
                playback(data) # Playing back the "Esc release" event
                return
            match data.value:
                case 1:
                    event = keyPressed(data)
                case 0:
                    event = keyReleased(data)
                case _:
                    pass
            if not event:
                playback(data)
        case _:
            pass

    if event:
        pass
    if not event:
        playback(data)

def playback(data):
    """Plays an event on ydotoold device"""
    ydotoold.write(data.type, data.code, data.value)
    ydotoold.write(enums.EV_SYN, 0, 0) # Writing a SYN event to make sure that the playback effect is immediate. Delay happens otherwise.


def cleanUp():
    """Cleans thread pool up"""
    print("Shutting down inputs thread pool...")
    eventsPool.shutdown()
