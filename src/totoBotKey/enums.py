from typing import Self

class Button:
    """Represents the values to send to ydotool."""
    BtnLeft = 0x00
    BtnRight = 0x01
    BtnMiddle = 0x02
    BtnSide = 0x03
    BtnExtra = 0x04
    BtnForward = 0x05
    BtnBack = 0x06
    BtnTask = 0x07
    MouseUp = 0x40
    MouseDown = 0x80

    @staticmethod
    def down(btn:Self):
        return btn + Button.MouseDown

    @staticmethod
    def up(btn:Self):
        return btn + Button.MouseUp

    @staticmethod
    def press(btn:Self):
        return btn + Button.MouseDown + Button.MouseUp


class Key:
    pass