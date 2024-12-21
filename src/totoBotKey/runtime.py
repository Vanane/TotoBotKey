"""Runtime
"""

import time
import signal
import evdevUtils
from ydotoolUtils import Ydotoold
from .parser import Parser, Keys
import totoBotKey.inputs as inputs


class Runtime:
    """_summary_"""

    ydo: Ydotoold = None
    running: bool

    def __init__(self):
        self.running = True

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
        evdevUtils.init()
        inputs.init()

        p = Parser.parseScript(script)

        if Parser.hasErrors():
            print(f"The following errors were found while parsing script '{script}' :")
            for e in Parser.getErrors():
                print(f"- {e}")
            return

        # Calling the script's initial setup
        p.pythonClass.init()

        # Starting to listen to devices
        evdevUtils.listenToAll(inputs.devEventCallback)

        self.running = True
        while self.running:
            time.sleep(1)

        print("Shutting down...")
        self.cleanUp()

    def cleanUp(self):
        """Cleans up"""
        print("Cleaning up...")
        evdevUtils.cleanUp()
        inputs.cleanUp()


if __name__ == "__main__":
    import sys

    Runtime().runWith(sys.argv[1])
