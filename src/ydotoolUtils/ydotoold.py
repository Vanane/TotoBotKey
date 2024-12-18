"""ytodoold"""

import subprocess


class Ydotoold:
    """Utils class for managing and controlling the ydotoold service"""

    ydotooldPidFile = "./pidFile.tmp"
    instructions: None

    def checkYdotooldStatus(self) -> int | None:
        """Checks whether the ydotoold service is running or not.

        Returns:
            int|None: the PID of the service, if running. None otherwise
        """
        try:
            return subprocess.check_output(["pidof", "ydotoold"])
        except Exception:
            return None
