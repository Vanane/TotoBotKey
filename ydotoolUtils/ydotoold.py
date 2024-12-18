import os, sys, time, signal
import subprocess

class Ydotoold():
    ydotooldPidFile = "./pidFile.tmp"
    instructions:None

    def checkYdotooldStatus(self):
        try:
            return subprocess.check_output(["pidof", "ydotoold"])
        except:
            return None

    def startYdotoold(self):
        returncode = subprocess.call(["/usr/bin/sudo", "ydotoold"])

        time.sleep(3)        
        os.system(f"pidof ydotoold > {self.ydotooldPidFile}")
        
        with open(self.ydotooldPidFile) as f:
            print(f"PID service ydotoold : {f.readline()}")

    def stopYdotoold(self):
        with open(self.ydotooldPidFile) as f:
            os.kill(int(f.read()), signal.SIGTERM)
        os.remove(self.ydotooldPidFile)


