# TotoBotKey
## Just like AutoHotKey !*
*with a $0 budget and 8 hours of work

## What is this ?
A scripting macro tool written in Python, mainly destined to Wayland (but it might work with Xorg too, ig ?).
The inputs are simulated using [ydotool](https://github.com/ReimuNotMoe/ydotool), whereas the events are managed simply by reading udev's input files.

It work not unsimilarly to AutoHotKey, which I've yet to find a satisfying replacement on Linux, and more specifically on Wayland.

## Why tho ?
I've yet to find a satisfying replacement on Linux, and more specifically on Wayland.
Apparently, KDE's macro tool is complete enough to do most stuff, but I believe that a single script ~~to rule them all~~ that handles everything feels easier to use and manage. Also, versioning™-capable !

## What do I need ?
- A computer and an OS that uses Wayland
- Python 3.9+
- [ydotool](https://github.com/ReimuNotMoe/ydotool), which also includes ydotoold

**Quick note on ydotoold :** (I AM NOT A SYSADMIN, DON'T TAKE THIS AS A GOOD SECURITY MEASURE)<br>
It is recommended to run it as root user, but by doing so, ydotoold will create a socket file that's unreadable by a normal user.

The way _I_ am running ydotoold right now is the following :
- Added myself to `input` group
- Added `export YDOTOOL_SOCKET='/tmp/.ydotool_socket'` in my `~.bashrc`
- A service runs `ydotoold -P 660 -o 0:<input GID>`

## How do I use it ?
Preferrably in a Python virtual environment :
```bash
python -m venv .venv
pip install totobotkey
```

See the `Script.md` file for detailed explanations and syntax.

See the `examples` directory for an example script and main file.

## To-do List
By order of priority :
- Refactor and clean codebase (lmao)
- Add support for each ydotool command options (delaying keys, sending keydown/up, etc.)
- Add keydown/keyup events
  - i'm starting to think that it doesn't make much sense
- Encapsulate decorations into a class
- Better handling of keyboard layout
  - Current solution : "you figure out your own keys dictionary"
  - Final solution : "let's use input.h because ydotool said so"
- Add a screenshot function (or a library that does just that on Wayland)
  - "You figure out your own screenshot function"
- Provide a basic GUI to manage running scripts
  - Maybe also a killswitch which you can activate with a shortcut, a click or just hovering your mouse above

## Known bugs
### TotoBotKey
- Every keypress combination needs a slight delay to be taken in account, in the domain of 50ms
- Keys might become locked in the held state under some circumstences :
  - Spamming keys _way_ too quickly
  - Holding keys while exiting the program
- The cursor's sensitivity seems to double when a script is running
  - I suspect that this is related to the fact that input events, including mouse movements, are played back on the ydotoold device which might not have the same settings than the original mouse device

### Ydotool
- `mousemove` command :
  - Option `absolute` seems broken on ydotool's side right now. A workaround consists in using two mousemove commands at once, one to set the cursor at (0,0), the other to move relatively to that.
    - This is managed by TotoBotKey
  - Distances in pixels seem to be doubled for no given reason. It's taken in account in the code, but still.
    - This might be an issue on multiple monitors settings, with mine having two 1920x1080 monitors. I've yet to test on another computer.
  - The cursor might not be able to move from one monitor to another, if you're using multiple monitors. The cursor would move relatively to the monitor it's present on.
