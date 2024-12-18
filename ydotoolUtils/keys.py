import os


class Keys():
    dumpFile = "./input-event-codes.h"
    keys:dict
    instance:object

    @staticmethod
    def getInstance():
        if not getattr(Keys, "instance", False):
            Keys.instance = Keys()
        return Keys.instance


    def __init__(self):
        if not os.path.exists(self.dumpFile):
            self.dumpKeys()
        
        self.registerKeys()
        Keys.instance = self
    

    def dumpKeys(self):
        
        print(f"Extracting keyCodes from `/usr/include/linux/input-event-codes.h` into `{self.dumpFile}`")

        os.system(f"cat /usr/include/linux/input-event-codes.h | gcc -dM -E - > {self.dumpFile}")
 
    
    def registerKeys(self):
        self.keys = dict()
        with open(self.dumpFile) as f:
            while l := f.readline().split():
                try:
                    self.keys[l[1]] = l[2]
                    setattr(Keys, l[1], l[2])
                except:
                    pass

    @staticmethod
    def getKey(key):
        return Keys.instance.keys[key]
    
    @staticmethod
    def getButton():
        pass
