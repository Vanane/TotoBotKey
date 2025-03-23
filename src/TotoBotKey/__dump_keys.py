"""Code generation for `keys.py` containing a dump of all Linux recognized keycodes."""
from os import system, remove, path
from io import FileIO
from sys import argv

DUMP_FILE = "./input-event-codes.h"

GENERATED_KEYS = "./keys.py"
GENERATED_BTNS = "./buttons.py"

TABS:dict


def build():
    global TABS
    TABS = {}

    dump_keys()

    generate_file()

def clean():
    for f in [GENERATED_KEYS, GENERATED_BTNS, DUMP_FILE]:
        if path.exists(f):
            remove(f)


def dump_keys():
    """Creates a cleaned local copy of the file located at
    `/usr/include/linux/input-event-codes.h`, for later use."""
    if not path.exists(DUMP_FILE):
        print(
            f"Extracting keyCodes from `/usr/include/linux/input-event-codes.h` into `{DUMP_FILE}`"
        )
        system(
            f"cat /usr/include/linux/input-event-codes.h | gcc -dM -E - > {DUMP_FILE}"
        )


def generate_file():
    """Reads `DUMP_FILE` as a file to generate the Keys enumeration
    of all keycodes that can be read and written in TotoBotKey.
    """
    with open(DUMP_FILE, encoding="utf-8") as f,\
    open(GENERATED_KEYS, mode="w", encoding="utf-8") as out_keys,\
    open(GENERATED_BTNS, mode="w", encoding="utf-8") as out_btns:
        write_class(out_keys, "Key")
        write_class(out_btns, "Button")

        while l := f.readline().split():
            try:
                if l[1].startswith('KEY_'):
                    l[1] = l[1].removeprefix('KEY_')
                    write_enum(out_keys, l[1], int(l[2]))
                else:
                    if l[1].startswith('BTN_'):
                        l[1] = l[1].removeprefix('BTN_')
                        write_enum(out_btns, l[1], int(l[2], 16 if l[2].startswith('0x') else 10))
                    else:
                        print(f"Not a key : '{l[1]}'")
            except ValueError:
                print(f"'{l[1]}' value unrecognized : '{l[2]}'")
            except IndexError:
                pass
            except Exception:
                pass
        write_class_end(out_keys)
        write_class_end(out_btns)


# File generation
def write_class(f:FileIO, clazz:str):
    """a"""
    global TABS
    f.write(f"class {clazz}:\n")
    TABS[f.fileno()] = 1
    pass

def write_class_end(f:FileIO):
    """Write class end"""
    global TABS
    TABS[f.fileno()] = 0
    f.write("")

def write_enum(f:FileIO, name:str, val:str):
    """Write enum"""
    if name[0].isdigit():
        name = '_' + name
    f.write(f"{indent(TABS[f.fileno()], tab=False)}{name} = {val}\n")

def indent(size:int, tab:bool=True, space:int=4):
    """Return indent"""
    return "".join(["\t" for i in range(0, size)] if tab else [" " for i in range(0, space * size)])



if __name__ == '__main__':
    locals()[argv[1]]()
