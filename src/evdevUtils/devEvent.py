import os, struct
from multiprocessing import Process

class DevEvent():
    listeners:dict
    keyboards:list
    mouses:list
    processes:list

    instance:object

    @staticmethod
    def getInstance():
        if not getattr(DevEvent, "instance", False):
            DevEvent.instance = DevEvent()
        return DevEvent.instance

    
    def __init__(self):
        devDir = '/dev/input/by-path'
        self.keyboards = list(filter(lambda d: d.endswith("-kbd"), os.listdir(devDir)))
        self.mouses = list(filter(lambda d:d.endswith("-mouse"), os.listdir(devDir)))
        self.processes = list()
       
        print("Detected devices :")
        for i in self.keyboards + self.mouses:
            print(f"- {str(i)}" )
        
        

    @staticmethod 
    def listenToAll(callback):
        for d in DevEvent.instance.keyboards + DevEvent.instance.mouses:
            p = Process(target=DevEvent.listen, args=(d,callback))
            p.start()
            print(f"Started listening on device '{d}'")

            DevEvent.instance.processes.append(p)


    @staticmethod
    def listen(dev, callback):
        with open(f"/dev/input/by-path/{dev}", 'rb') as f:
            while True:
                data = f.read(24)
                data = struct.unpack('4IHHI', data)
                callback(data)                
        return None


    @staticmethod
    def addListener(lis, dev):
        if not DevEvent.instance.listeners.get(dev, False):
            DevEvent.instance.listeners[dev] = list()
        DevEvent.instance.listeners[dev].append(lis)

