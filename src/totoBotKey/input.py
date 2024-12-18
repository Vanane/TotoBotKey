"""input
"""

from typing import Callable, Self
from evdevUtils import enums

EV = "EVENTS"


class InputManager:
    """Singleton class to manage event inputs received from DevEvent"""

    events: dict
    keyPresses: dict

    """
    Keys that will be released artificially at the next event catch
    """
    toBeReleased: list

    instance: object

    @staticmethod
    def getInstance() -> Self:
        """Returns the singleton's instance"""
        if not getattr(InputManager, "instance", False):
            InputManager.instance = InputManager()
        return InputManager.instance

    def __init__(self):
        self.keyPresses = dict()
        self.btnPresses = dict()
        self.events = dict()

    def keyPressed(self, keyCode: int):
        """The given keycode is flagged as currently held down in the keyPresses dict.
        Called whenever an input event is caught, and the "value" field equals 1.
        """
        self.keyPresses[keyCode] = True

        self.checkUserEvents()

    def keyReleased(self, keyCode: int):
        """The given keycode is removed from the keyPresses dict.
        Called whenever an input event is caught, and the "value" field equals 0.
        """
        self.keyPresses.pop(keyCode, None)

        self.checkUserEvents()

    def checkUserEvents(self):
        """Checks out if, with the keys currently present in keyPresses,
        an user-defined event  can be triggered.
        """
        event = "+".join(sorted(map(str, self.keyPresses)))
        print(f"Trying to call event '{event}'")
        if self.events.get(event, False):
            self.events[event]()
            print(f"Event '{event}' called successfully")

    @staticmethod
    def addEvent(comb: str, f: Callable):
        """Adds an user-defined event to the manager.

        Args:
            comb (str): combination of keycodes that should trigger the function,
            in this format : xx+yy+zz
            f (_type_): function to call in reaction to this event
        """
        InputManager.instance.events[comb] = f
        print(f"Event '{comb}' added")

    @staticmethod
    def devEventCallback(data: tuple):
        """Callback that's called by DevEvent whener any input events occurs on any devices.
        It will manage keys states, and event triggering when necessary

        Args:
            data (tuple): Event data, as defined in the Linux [Userspace API](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/include/uapi/linux/input.h)
        """

        match int(data[4]):
            case enums.EV_KEY:
                if data[6] == 1:
                    print(f"Received event : '{data}'")
                    InputManager.instance.keyPressed(data[5])
                else:
                    if data[6] == 0:
                        InputManager.instance.keyReleased(data[5])
            case _:
                pass
