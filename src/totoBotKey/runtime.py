"""Runtime
"""

import time
import signal
import evdevUtils
from ydotoolUtils import ydotoold, keys
from . import parser
from . import inputs


running: bool


def __init__():
    global running
    running = True


def runWith(script: str):
    """Runs TotoBotKey with a given script name, assuming the name
    doesn't contain the file extension

    Args:
        script (str): name of the script to load
    """
    global running

    if not ydotoold.checkYdotooldStatus():
        print("ytodoold service not running, exiting.")
        exit()

    keys.init()
    evdevUtils.init()
    inputs.init()
    parser.init()
    p = parser.parseScript(script)

    if parser.hasErrors():
        print(f"The following errors were found while parsing script '{script}' :")
        for e in parser.getErrors():
            print(f"- {e}")
        return

    # Calling the script's initial setup
    p.pythonClass.init()

    # Starting to listen to devices
    evdevUtils.listenToAll(inputs.devEventCallback)

    running = True
    while running:
        time.sleep(1)

    print("Shutting down...")
    cleanUp()


def cleanUp():
    """Cleans up"""
    print("Cleaning up...")
    evdevUtils.cleanUp()
    inputs.cleanUp()


if __name__ == "__main__":
    import sys

    runWith(sys.argv[1])
