"""Runtime
"""
import evdevUtils
from ydotoolUtils import ydotoold
from totoBotKey import keys, parser, inputs


running: bool

def __init__():
    """Initializes the runtime environment"""
    global running
    running = False


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

    evdevUtils.subscribeToAll(inputs.callback)

    running = True

    # Starting to listen to devices, blocking the main thread
    evdevUtils.listen()

    running = False

    cleanUp()


def cleanUp():
    """Cleans up"""
    print("Shutting down...")
    inputs.cleanUp()
    evdevUtils.cleanUp()


if __name__ == "__main__":
    import sys

    runWith(sys.argv[1])
