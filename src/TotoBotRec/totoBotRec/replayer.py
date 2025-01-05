from .recorder import Record, RecordType

def getMacro(records:list[Record]):
    """"""
    for r in records:
        print(f"{r.type_}({', '.join(r.args)})")
    pass