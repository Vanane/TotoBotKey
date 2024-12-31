"""ytodoold"""

import subprocess


ydotooldPidFile = "./pidFile.tmp"
instructions: None


def checkYdotooldStatus() -> int | None:
    """Checks whether the ydotoold service is running or not.

    Returns:
        int|None: the PID of the service, if running. None otherwise
    """
    try:
        return subprocess.check_output(["pidof", "ydotoold"])
    except Exception:
        return None
