"""To run it directly from the git repository, use :
    `PYTHONPATH=PYTHONPATH:../src python main.py`
"""

from totoBotKey.runtime import Runtime
import signal

def sigint(s, f):
    r.stopFlag = True

r = Runtime()

signal.signal(signal.SIGINT, sigint)

r.runWith("myScript")
