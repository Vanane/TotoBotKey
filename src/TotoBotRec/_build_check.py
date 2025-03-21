"""Python script to check conditions needed to build the package."""
from inspect import getmembers, isfunction

import totoBotKey.commands as commands
import totoBotRec.replayer as replayer


def checkReplayerImplementsAllCommands():
    for fn in getmembers(commands, isfunction):
        print(fn)


def check():
    checkReplayerImplementsAllCommands()
pass

if __name__ == "__main__":
    check()
