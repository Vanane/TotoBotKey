"""devEvent
"""

import os
import time
import struct
import evdev
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Callable, List


"""DevEvent is a singleton class that manages subscription
to the computer's hardware devices and listens to their input events.
"""

DEV_DIR = "/dev/input/by-id/"

listeners: dict

devices: list

ydotoold: object

devicePool: ThreadPoolExecutor
deviceFutures: List[Future]
running: bool

instance: object


def init():
    global running, devices, deviceFutures, devicePool
    running = False
    deviceFutures = list()
    devices = list()


def listenToAll(callback: Callable):
    """Runs as many processes as there are detected hardware mouses and keyboards,
    to subscribe and then listen to any of their input events.

    Args:
        callback (function): function that will handle any input events occuring on any hardware
    """
    global running, devices, deviceFutures, devicePool

    devNames = list(filter(lambda d: d.endswith("-kbd"), os.listdir(DEV_DIR))) + list(
        filter(lambda d: d.endswith("-mouse"), os.listdir(DEV_DIR))
    )

    devicePool = ThreadPoolExecutor(max_workers=10)

    print("Initializing devices...")
    running = True
    for d in devNames:
        try:
            devices.append(dev := evdev.InputDevice(f"{DEV_DIR}{d}"))
            print(f"- {dev.name}")
        except OSError as e:
            print(e)

    listen(callback)


def listen(callback: Callable) -> None:
    """Subscribes to a given device's input events, then listens to it indefinitely"""
    global devicePool

    for dev in devices:
        time.sleep(1)
        dev.grab()

    while running:
        for dev in devices:
            data = dev.read_one()
            if data:
                devicePool.submit(callback, data)

    for dev in devices:
        dev.ungrab()


def cleanUp():
    print("Shutting down devEvent thread pool...")
    for f in deviceFutures:
        f.join()
        f.close()
    devicePool.shutdown()


def getDevices(predicate, fromDir="/dev/input"):
    devs = [evdev.InputDevice(d) for d in evdev.list_devices(fromDir)]
    r = list(filter(predicate, devs))
    if len(r) == 1:
        return r[0]
    return r
