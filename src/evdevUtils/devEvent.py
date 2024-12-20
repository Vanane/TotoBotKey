"""devEvent
"""

import os
import time
import struct
import evdev
from multiprocessing import Process
from typing import Callable, Self


class DevEvent:
    """DevEvent is a singleton class that manages subscription
    to the computer's hardware devices and listens to their input events.
    """

    listeners: dict
    keyboards: list
    mouses: list
    processes: list
    stopFlag: bool

    instance: object

    @staticmethod
    def getInstance() -> Self:
        """Get the singleton instance."""
        if not getattr(DevEvent, "instance", False):
            DevEvent.instance = DevEvent()
        return DevEvent.instance

    def __init__(self):
        devDir = "/dev/input/by-path"
        self.keyboards = list(filter(lambda d: d.endswith("-kbd"), os.listdir(devDir)))
        self.mouses = list(filter(lambda d: d.endswith("-mouse"), os.listdir(devDir)))
        self.processes = list()
        self.stopFlag = False

        print("Detected devices :")
        for i in self.keyboards + self.mouses:
            print(f"- {str(i)}")

    @staticmethod
    def listenToAll(callback: Callable):
        """Runs as many processes as there are detected hardware mouses and keyboards,
        to subscribe and then listen to any of their input events.

        Args:
            callback (function): function that will handle any input events occuring on any hardware
        """
        for d in DevEvent.instance.keyboards + DevEvent.instance.mouses:
            p = Process(target=DevEvent.listen, args=(d, callback))
            p.start()
            print(f"Started listening on device '{d}'")

            DevEvent.instance.processes.append(p)

    @staticmethod
    def listen(dev: str, callback: Callable) -> None:
        """Subscribes to a given device's input events, then listens to it indefinitely

        Args:
            dev (str): name of the device (as seen in `/dev/input/by-path`) to subcribe to
            callback (function): function that will handle any input events occuring on
            this hardware

        Returns:
            None
        """
        with open(f"/dev/input/by-path/{dev}", "rb") as f:
            while True:
                data = f.read(24)
                (tv_sec, tv_sec_l, tv_usec, tv_usec_l, type, code, value) = (
                    struct.unpack("4IHHI", data)
                )
                callback(tv_sec, tv_usec, type, code, value)
        return None

    @staticmethod
    def cleanUp():
        DevEvent.instance.stopFlag = True
        for f in DevEvent.instance.processes:
            f.terminate()
