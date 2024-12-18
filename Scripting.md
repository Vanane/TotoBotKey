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

## Events
TotoBotkey defines two decorators for your script functions : @on and @onExplicit.
It allows for a quick binding between a given function and an event listener to a given key combination.

**The parser will assume all of event-bound functions are static.**

### @on
@on takes a single argument, which mimmicks the syntax of AutoHotKey's own...Hot keys.
This allows for quick, but otherwise fairly incomplete bindings.

Each character either represents the alphanumerical character that you want to listen to, or a modifier key (Ctrl, Alt, Shift, Super).
Giving several characters allows to listen for a specific combination of keystrokes.

|Character|Visual representation|Keycode representation|
|---|---|---|
|[a-z0-9]|A, B, C ... And the number row above the alphabet|KEY_A, KEY_B, KEY_C ... KEY_0, KEY_1 ...|
|^|Left Ctrl|KEY_LEFTCTRL (29)|
|+|Left Shift|KEY_LEFTSHIFT (42) |
|!|Left Alt|KEY_LEFTALT (56)|
|#|Menu/Super/Windows key|KEY_MENU (125)|
|BtnLeft, BtnRight, BtnWheel, Btn4, Btn5|Physical buttons of the mouse|BTN_LEFT, BTN_RIGHT, BTN_WHEEL, BTN_4, BTN_5|

Additional keywords might be supported if I feel the need for it. Otherwise, @onExplicit is a catch-all alternative.

### @onExplicit
@onExplicit takes a single argument that allows for explicit keycode combination.
Many keys, such as Delete, Insert, Num Lock, etc., are difficult to interpret, unless thair names are hard-written in the parser (such as `BtnLeft` above).<br>
@onExplicit gives a way to pass a combination of keycodes directly and avoid parsing an expression, while also giving full flexibility.

Each keycode must be separated by a `+` character.

Example : `29+25` will bind to `Ctrl+P`

## Example
```py
from totoBotKeys import *

class MyScript(BaseScript):

    @on("^a")
    @staticmethod
    def doSmth():
        type("Ctrl+A has been pressed")
    

    @on("!a")
    @staticmethod
    def doSmth2():
        type("Shift+A has been pressed")
        wait(1000)
        type("One second has passed")
    
    @staticmethod
    def init():
        print("This is the script's initiation code")


```
