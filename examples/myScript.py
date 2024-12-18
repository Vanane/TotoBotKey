from totoBotKey import *

class MyScript(BaseScript):

    @on("^a")
    @staticmethod
    def doSmth():
        type("Ctrl+A got hit")
    

    @on("!a")
    @staticmethod
    def doSmth2():
        type("Shift + A got hit")
        wait(1000)
        type("One second has passed")
    
    @staticmethod
    def init():
        print('innit')

