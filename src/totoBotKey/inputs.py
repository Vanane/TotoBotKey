"""input
"""

from concurrent.futures import Future, ThreadPoolExecutor
from multiprocessing.managers import SharedMemoryManager
from typing import Callable, List
from evdevUtils import enums, getDevices, listener
from . import runtime
import os
import signal

EV = "EVENTS"


"""Singleton class to manage event inputs received from DevEvent"""

events: dict
keyPresses: dict

eventFutures: List[Future]
eventsPool: ThreadPoolExecutor
sharedMem: SharedMemoryManager

ydotoold: object


def init():
    global keyPresses, events, eventFutures, eventsPool, sharedMem, ydotoold

    keyPresses = dict()
    events = dict()
    eventFutures = list()

    eventsPool = ThreadPoolExecutor(max_workers=10)

    ydotoold = getDevices(lambda d: d.name == "ydotoold virtual device")


def keyPressed(data) -> bool:
    """The given keycode is flagged as currently held down in the keyPresses dict.
    Called whenever an input event is caught, and the "value" field equals 1.
    """
    keyPresses[data.code] = True
    return callEvent()


def keyReleased(data) -> bool:
    """The given keycode is removed from the keyPresses dict.
    Called whenever an input event is caught, and the "value" field equals 0.
    """
    keyPresses.pop(data.code, None)
    return False


def callEvent(ev: str = None) -> bool:
    """Tries to find and call a given user event, not generating any error in the absence of one."""
    try:
        if ev is None:
            return callEvent("+".join(sorted(map(str, keyPresses))))

        for f in eventFutures:
            if f.done():
                eventFutures.remove(f)

        print(f"Trying to call event '{ev}'")
        if events.get(ev, False):
            eventFutures.append(f := eventsPool.submit(eventThread, events[ev]))
            print(f"Event '{ev}' called successfully through Future {str(f)}")
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def eventThread(event: Callable):
    try:
        event()
    except Exception as e:
        print(e)


def isPressed(key):
    """Return the state of a given keycode"""
    return keyPresses.get(int(key), False)


def addEvent(comb: str, f: Callable):
    """Adds an user-defined event to the manager.

    Args:
        comb (str): combination of keycodes that should trigger the function,
        in this format : xx+yy+zz
        f (_type_): function to call in reaction to this event
    """
    events[comb] = f
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
        case _:
            pass

    if event:
        pass
    else:
        playback(data)

def playback(data):
    """Plays an event on ydotoold device"""
    ydotoold.write_event(data)


def cleanUp():
    """Cleans thread pool up"""
    print("Shutting down inputs thread pool...")
    eventsPool.shutdown()
