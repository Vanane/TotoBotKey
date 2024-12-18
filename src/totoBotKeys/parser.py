from ydotoolUtils import Keys


class BaseScript():
    '''Class to inherit any script from'''

    def main(self):
        '''Main script that will be called at the beginning.'''
        pass
    pass


class Parser():
    def getErrors():
        if Parser.hasErrors():
            return Parser.errors
        return None


    def addError(msg):
        if not hasattr(Parser, "errors"):
            Parser.errors = list()
        Parser.errors.append(msg)


    def hasErrors():
        return hasattr(Parser, "errors")
    

    def parseScript(mod) -> type:        
        clss:type = Parser.getScriptClassReflect(mod)
        if clss is None:
            print("No script found.")
            return False
        
        print(f"Script found : {clss.__name__}")

        return ParserResult(clss, Parser.getErrors(), False)


    def parseEventDecorator(bind:str):
        '''
        Case insensitive
        Bind examples :
            "a" : Key A
            "^a" : Ctrl + Key A
            "^!a" : Ctrl + Alt + Key A
            "abc" : Keys A + B + C 
        '''
        modsDict = {"^":Keys.KEY_LEFTCTRL, "+":Keys.KEY_LEFTSHIFT, "!":Keys.KEY_LEFTALT, "#":Keys.KEY_MENU}
        keysDict = {"BtnLeft":Keys.BTN_LEFT, "BtnRight":Keys.BTN_RIGHT,"BtnWheel":Keys.BTN_WHEEL,"Btn4":Keys.BTN_4, "Btn5":Keys.BTN_5}

        mods = set()
        chars = set()
        
        bind = bind.lower()
        i = 0
        while i < len(bind):
            l = bind[i]
            if modsDict.get(l, False):
                mods.add(modsDict[l])
            else:
                t = ""
                for j in range(len(bind[i:])):
                    k = bind[i+j]                    
                    if k.isalnum():
                        t += k
                    if not k.isalnum() or len(bind[i:]) == j+1:
                        key = f"KEY_{t.upper()}"
                        try:                            
                            chars.add(keysDict.get(t, getattr(Keys, key)))
                        except AttributeError:
                            Parser.addError(f"Error : Key '{key}' not found when trying to parse expression '{bind}'.")
                        i += j                        
                        break
            i+=1

        return (sorted(chars), sorted(mods))



    def getScriptClassReflect(mod):
        for i in mod.__dict__:
            attr:type = mod.__getattribute__(i)
            if type(attr) == type(type) and attr.__bases__.__contains__(BaseScript):
                return attr


class ParserResult():
    pythonClass:type
    errors:list
    isAsync:bool


    def __init__(self, p, e, a):
        self.pythonClass = p
        self.errors = e
        self.isAsync = a