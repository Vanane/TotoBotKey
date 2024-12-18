from evdevUtils import enums
EV = "EVENTS"

class InputManager():
    events:dict    
    keyPresses:dict

    '''
    Keys that will be released artificially at the next event catch
    '''
    toBeReleased:list

    instance:object


    @staticmethod
    def getInstance():
        if not getattr(InputManager, "instance", False):
            InputManager.instance = InputManager()
        return InputManager.instance


    def __init__(self):
        self.keyPresses = dict()
        self.btnPresses = dict()
        self.events = dict()


    def keyPressed(self, keyCode):
        self.keyPresses[keyCode] = True
        
        self.checkUserEvents()


    def keyReleased(self, keyCode):
        self.keyPresses.pop(keyCode, None)

        self.checkUserEvents()


    def checkUserEvents(self):
        event = "+".join(sorted(map(str, self.keyPresses)))
        print(f"Trying to call event '{event}'")
        if self.events.get(event, False):
            self.events[event]()
            print(f"Event '{event}' called successfully")


    @staticmethod
    def addEvent(comb, f):
        InputManager.instance.events[comb] = f
        print(f"Event '{comb}' added")


    @staticmethod
    def devEventCallback(data:tuple):
        
        match int(data[4]):
            case enums.EV_KEY:
                if data[6] == 1:
                    print(f"Received event : '{data}'")
                    InputManager.instance.keyPressed(data[5])
                else:
                    if data[6] == 0:
                        InputManager.instance.keyReleased(data[5])
            case _:
                pass
