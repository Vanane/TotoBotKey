from ydotoolUtils import *
from .parser import *
from .input import *
import importlib
from evdevUtils import *
from multiprocessing import Process

class Runtime():
    ydo:Ydotoold = None
    
    def runWith(self, script):
        self.ydo = Ydotoold()

        if not self.ydo.checkYdotooldStatus():
            print("ytodoold service not running, exiting.")
            exit()

        Keys.getInstance()
        DevEvent.getInstance()
        InputManager.getInstance()

        p = Parser.parseScript(importlib.import_module(script))
        
        if Parser.hasErrors():
            print(f"The following errors were found while parsing script '{script}' :")
            for e in Parser.getErrors():
                print(f"- {e}")
            exit()

        # Starting to listen to devices
        DevEvent.listenToAll(InputManager.devEventCallback)

        # Instantiating user script
        a = p.pythonClass()


        '''
        process = Process(target=a.main)
        process.start()
        
        process.join()
        '''

        # End of program
        self.cleanUp()



    def cleanUp(self):
        pass


    def dispatchEvent(self, data):
        pass



if __name__ == "__main__":
    import sys
    Runtime().runWith(sys.argv[1])