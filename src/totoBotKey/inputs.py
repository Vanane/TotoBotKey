"""input
"""

from concurrent.futures import Future, ThreadPoolExecutor
from multiprocessing.managers import SharedMemoryManager
from typing import Callable, List
from evdevUtils import enums

EV = "EVENTS"


"""Singleton class to manage event inputs received from DevEvent"""

events: dict
keyPresses: dict

futures: List[Future]
eventsPool: ThreadPoolExecutor
sharedMem: SharedMemoryManager

"""
Keys that will be released artificially at the next event catch
"""
toBeReleased: list

instance: object


def init():
    global keyPresses, events, futures, eventsPool, sharedMem

    keyPresses = dict()
    events = dict()
    futures = list()

    eventsPool = ThreadPoolExecutor(max_workers=5)


def keyPressed(keyCode: int):
    """The given keycode is flagged as currently held down in the keyPresses dict.
    Called whenever an input event is caught, and the "value" field equals 1.
    """
    keyPresses[keyCode] = True
    callEvent("+".join(sorted(map(str, keyPresses))))


def keyReleased(keyCode: int):
    """The given keycode is removed from the keyPresses dict.
    Called whenever an input event is caught, and the "value" field equals 0.
    """
    keyPresses.pop(keyCode, None)


def callEvent(ev: str):
    """Tries to find and call a given event, not generating any error in the absence of one."""
    for f in futures:
        if f.done():
            futures.remove(f)

    if events.get(ev, False):
        futures.append(f := eventsPool.submit(eventThread, events[ev]))
        print(f"Event '{ev}' called successfully through Future {str(f)}")


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


def devEventCallback(s, ms, evType, code, value):
    """Callback that's called by DevEvent whener any input events occurs on any devices.
    It will manage keys states, and event triggering when necessary

    Args:
        data (tuple): Event data, as defined in the Linux [Userspace API](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/include/uapi/linux/input.h)
    """
    # print((s, ms, evType, code, value))

    match int(evType):
        case enums.EV_KEY:
            match value:
                case 1:
                    print(f"Received event : '{(s, ms, evType, code, value)}'")
                    keyPressed(code)
                case 0:
                    keyReleased(code)
                case _:
                    pass
        case _:
            pass


def cleanUp():
    eventsPool.shutdown()
