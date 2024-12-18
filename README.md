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

You will need either root access to start ydotoold, or make it a service like so :<br>
(I'm not a sysadmin, don't take this as a good security practice in any ways)
```
[Unit]
Description=ydotoold
Documentation=https://github.com/ReimuNotMoe/ydotool
After=network.target
 
[Service]
User=root
ExecStart=ydotoold
Restart=on-failure   
 
[Install]
WantedBy=multi-user.target
```

## To-do List
By order of priority :
- Refactor and clean codebase (lmao)
- Add support for each ydotool command options (delaying keys, sending keydown/up, etc.)
- Add keydown/keyup events
- Encapsulate decorations into a class
- Better handling of keyboard layout
- Add a screenshot function (or a library that does just that on Wayland)