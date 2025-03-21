from .recorder import Record, RecordType
from totoBotKey.commands import clickAt, holding, key, keydown, keyup, mousemove, pressKeys, type_, wait


def getMacro(records:list[Record]):
    """"""
    for r in records:
        print(f"{r.type_}({', '.join(r.args)})")
    pass


def _getClickAt():
    pass