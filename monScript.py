from totoHotKeys import *

class MyScript(BaseScript):

    @on("^a")
    @staticmethod
    def doSmth():
        type("prout")
    

    @on("!a")
    @staticmethod
    def doSmth2():
        type("troup")
        wait(500)
        type("prout")
    
    @staticmethod
    def main():
        print('script ok')

