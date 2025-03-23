"""Code generation for `keys.py` containing a dump of all Linux recognized keycodes."""
from os import system, remove, path
from io import FileIO
from sys import argv
from ast import literal_eval
from __codegen import PythonCodeGen

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
        gen_keys = PythonCodeGen(out_keys, indent_string=" "*4)
        gen_btns = PythonCodeGen(out_btns, indent_string=" "*4)
        with gen_keys.cls("Key"), gen_btns.cls("Button"):

            while l := f.readline().split():
                try:
                    if l[1].startswith('KEY_'):
                        l[1] = l[1].removeprefix('KEY_')
                        write_enum(gen_keys, l[1], literal_eval(l[2]))
                    else:
                        if l[1].startswith('BTN_'):
                            l[1] = l[1].removeprefix('BTN_')
                            write_enum(gen_btns, l[1], literal_eval(l[2]))
                        else:
                            pass#print(f"Not a key : '{l[1]}'")
                except ValueError:
                    pass#print(f"'{l[1]}' value unrecognized : '{l[2]}'")
                except IndexError:
                    pass
                except Exception as e:
                    print(e)
                    pass


# File generation
def write_enum(f:PythonCodeGen, name:str, val:str):
    """Write enum"""
    if name[0].isdigit():
        name = '_' + name
    f.prop(name, val=val)


if __name__ == '__main__':
    locals()[argv[1]]()
