"""To run it directly from the git repository, use :
    `PYTHONPATH=PYTHONPATH:../src python main.py`
"""

import signal
from totoBotKey.runtime import Runtime


r = Runtime()

r.runWith("myScript")

