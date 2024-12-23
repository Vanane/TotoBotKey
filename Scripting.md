# Scripting Guide
TotoBotKey allows for Python-based macro scripting, including basically everything Python has to offer.
It implements basic keystrokes and mouse clicks, as well as some additional functions. These are passed to and managed by ydotool.
it also implements events detection to some extend. These are managed by the evdevUtils package.

**Since a good portion of it is based on ydotools, the same keyboard limitations and workarounds may apply.**

# Beninging
Any script must inherit from the totoBotKeys.parser.BaseScript class, as that is how TotoBotKey's parser will identify it and interpret its contents.

**Any scripts that inherits this class must be thought of as static, or written as a singleton. References to `self` aren't supported for now.**

## Ydotool
*Docs about [ydotool](https://github.com/ReimuNotMoe/ydotool) can be found on their Github repository directly.*

This part will address what's supported by TotoBotKey, and not ydotool's capabilities.

ydotool defines several commands to simulate device inputs. 
### type
Allows to write text directly, rather than send keystrokes one after the other.

Options : No options yet.

### key
Sends a single keypress (keydown + keyup) from a given keycode. See your local `/usr/include/linux/input-event-codes.h` for an exhaustive list of your keycodes, as their codes are all but in natural order.

Options : No options yet.

### click
Simulates a click at a given position on the viewport, the viewport being the whole space shaped by all of your monitors (prolly broken rn).

Options : No options yet.

### mousemove
Moves the mouse across the viewport (prolly broken too).

Options : No options yet.

Known bugs :
- Option `absolute` is broken on ydotool's side right now. A workaround consists in using two mousemove commands at once, one to set the cursor at (0,0), the other to move relatively to that.
- Distances in pixels seem to be doubled for no given reason. It's taken in account in the code, but still.
    - This might be an issue on multiple monitors settings
- The cursor might not be able to move from one monitor to another, if you're using multiple monitors. The cursor would move relatively to the monitor it's present on.

## Namespaces
There are several modules to import in order to script properly :
```py
from totoBotKey.parser import BaseScript                        # Class to inherit the script from
from totoBotKey.inputs import isPressed                         # Control functions to check key and event states
from totoBotKey.decorators import on, onRaw, BindType           # Function decorators and enums associated with it
from totoBotKey.enums import Key, Button                        # Input-event-codes.h key and button enums (created dynamically)
from totoBotKey.commands import type_, click, wait, clickAt     # Ydotool and additionnal automation functions
```

## Events
TotoBotkey defines two decorators for your script functions : @on and @onRaw.
It allows for a quick binding between a given function and an event listener to a given key combination.

**The parser will assume all of event-bound functions are static.**

### @on
@on takes N arguments, each corresponding to a combination of modifiers and one key to bind a function to. It uses a syntax similar to the syntax of AutoHotKey's own...Hot keys.
This allows for quick, but fairly incomplete bindings.

Although each argument can be given with its own modifiers, the final binding will accumulate all the modifiers and apply to all of the keys given.

Each character either represents the alphanumerical character that you want to listen to, or a modifier key (Ctrl, Alt, Shift, Super).
Giving several characters allows to listen for a specific combination of keystrokes.

|Character|Visual representation|Keycode representation|
|---|---|---|
|[a-z0-9]|A, B, C ... And the number row above the alphabet|KEY_A, KEY_B, KEY_C ... KEY_0, KEY_1 ...|
|^|Left Ctrl|KEY_LEFTCTRL (29)|
|+|Left Shift|KEY_LEFTSHIFT (42) |
|!|Left Alt|KEY_LEFTALT (56)|
|#|Menu/Super/Windows key|KEY_MENU (125)|
|BtnLeft, BtnRight, BtnWheel, Btn4, Btn5, BtnSide, BtnExtra|Physical buttons of the mouse|BTN_LEFT, BTN_RIGHT, BTN_WHEEL, BTN_4, BTN_5, BTN_SIDE, BTN_EXTRA|

Additional keywords might be supported if I feel the need for it. Otherwise, @onExplicit is a catch-all alternative.

Examples :
```py
# When Ctrl+Shift+P is pressed, do something
@on("^+p") 
@staticmethod
def doSmth():
    # Do smth...

# When Ctrl+Shift+A+B+C is pressed, do something
@on("a", "^b", "+c") 
@staticmethod
def doSmth():
    # Do smth...    
```

#### Bind types
@on also accepts a named `bType` argument.
When set to `BindType.ANY`, a binding will be able to trigger whenever its keys are pressed, without regard for any other key state.
When set to `BindType.ONLY`, a binding will only trigger specifically when its keys are all pressed, and nothing else.

Examples :
```py
# This will trigger only when A, and only A, gets pressed. No other combination will work : Ctrl+A, Shift+A, A+B, A+LeftClick...
@on("a") 
@staticmethod
def pressA():
    # Do smth...

# This will trigger whenever A gets pressed, independently from any other key.
@on("a", bType=BindType.ANY) 
@staticmethod
def pressAnyA():
    # Do smth...

# Which means that when this binding triggers, pressAnyA() most likely will trigger as well, since A was pressed.
@on("^a") 
@staticmethod
def pressCtrlA():
    # Do smth...
```

### @onRaw
@onRaw takes N arguments that allows for explicit keycode combination.
Many keys, such as Delete, Insert, Num Lock, etc., are difficult to interpret, unless thair names are hard-written in the parser (such as `BtnLeft` above).<br>
@onRaw gives a way to pass a combination of keycodes directly and avoid parsing an expression, while also giving full flexibility.

Each keycode must be separated by a `+` character.

Examples :
```py
# When Ctrl+Shift+P is pressed, do something
@onRaw(KEY_LEFTCTRL, KEY_LEFTSHIFT, KEY_P)
@staticmethod
def doSmth():
    # Do smth...
```
#### Bind types
Just as @on, @onRaw also takes a `bType` argument, and the same effects apply.