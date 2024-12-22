"""devEvent"""

import os
import time
from evdev import InputDevice, list_devices
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Callable, List

DEV_DIR = "/dev/input/by-id/"
"""Directory to read the devices from"""

devices: List[InputDevice]
"""List of active devices that will be listened"""

ydotoold: object
"""InputDevice that is used by the ydotoold service to write events"""

devicePool: ThreadPoolExecutor
"""Thread pool for treating devices input events"""
deviceFutures: List[Future]
"""List of Futures emitted by the thread pool"""

running: bool
"""State of the global program. Each thread will try to interrupt itself when running gets to False"""
 
callback:Callable
"""Callable function that will handle input events"""

def init():
    """Initializing the device events manager module"""
    global running, devices, deviceFutures, devicePool
    running = False
    deviceFutures = list()
    devices = list()


def subscribeToAll(cb: Callable):
    """Runs as many processes as there are detected hardware mouses and keyboards,
    to subscribe and then listen to any of their input events.

    Args:
        cb (function): function that will handle any input events occuring on any hardware
    """
    global devices, deviceFutures, devicePool, callback

    callback = cb

    print("Initializing devices...")

    devNames = list(filter(lambda d: d.endswith("-kbd"), os.listdir(DEV_DIR))) + list(
        filter(lambda d: d.endswith("-mouse"), os.listdir(DEV_DIR))
    )

    for d in devNames:
        try:
            devices.append(dev := InputDevice(f"{DEV_DIR}{d}"))
            print(f"- {dev.name}")
        except OSError as e:
            print(e)
    
    time.sleep(1) # Small sleep in order to read all the events that occured while opening the devices



def listen() -> None:
    """Subscribes to a given device's input events, then listens to it indefinitely"""
    global devicePool, devices, running, callback

    devicePool = ThreadPoolExecutor(max_workers=20)

    for dev in devices:
        dev.grab()
    
    print("Ready !")

    running = True

    try:
        while running:
            for dev in devices:
                data = dev.read_one()
                if data:
                    devicePool.submit(callback, data)
    except Exception as e:
        print(e)
        running = False
        
    for dev in devices:
        dev.ungrab()


def cleanUp():
    """Cleans up the devices and threads used by the module"""
    global devicePool, deviceFutures, devices, running
    running = False
    print("Shutting down listener thread pool...")
    for f in deviceFutures:
        while f.running():
            time.sleep(100)
    for d in devices:
        d.close()
    devicePool.shutdown()


def getDevices(predicate, fromDir="/dev/input"):
    """Returns InputDevice devices located in <fromDir> and filtered by <predicate>"""
    devs = [InputDevice(d) for d in list_devices(fromDir)]
    r = list(filter(predicate, devs))
    if len(r) == 1:
        return r[0]
    return r
