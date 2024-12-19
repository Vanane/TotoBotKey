"""To run it directly from the git repository, use :
    `PYTHONPATH=PYTHONPATH:../src python main.py`
"""

from totoBotKey.runtime import Runtime
import signal

r = Runtime()


def sigint(s, f):
    r.stopFlag = True


signal.signal(signal.SIGINT, sigint)

r.runWith("myScript")
