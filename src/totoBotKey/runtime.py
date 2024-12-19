"""Runtime
"""

import signal
from evdevUtils import DevEvent
from ydotoolUtils import Ydotoold
from .parser import Parser, Keys
from .input import InputManager


class Runtime:
    """_summary_"""

    ydo: Ydotoold = None
    stopFlag: bool

    def __init__(self):
        self.stopFlag = False
        pass

    def runWith(self, script: str):
        """Runs TotoBotKey with a given script name, assuming the name
        doesn't contain the file extension

        Args:
            script (str): name of the script to load
        """
        self.ydo = Ydotoold()

        if not self.ydo.checkYdotooldStatus():
            print("ytodoold service not running, exiting.")
            exit()

        Keys.getInstance()
        DevEvent.getInstance()
        InputManager.getInstance()

        p = Parser.parseScript(script)

        if Parser.hasErrors():
            print(f"The following errors were found while parsing script '{script}' :")
            for e in Parser.getErrors():
                print(f"- {e}")
            return

        # Calling the script's initial setup
        p.pythonClass.init()

        # Starting to listen to devices
        DevEvent.listenToAll(InputManager.devEventCallback)

        while not self.stopFlag:
            pass

        self.cleanUp()

    def cleanUp(self):
        """Cleans up"""        
        DevEvent.cleanUp()
        InputManager.cleanUp()


if __name__ == "__main__":
    import sys

    Runtime().runWith(sys.argv[1])
