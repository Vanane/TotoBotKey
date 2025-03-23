from io import IOBase
import contextlib

class PythonCodeGen:
    def __init__(self, f: IOBase, indent_string="\t", newline="\n"):
        self.file = f
        self.indent = 0
        self.indent_string = indent_string
        self.newline = newline
    @contextlib.contextmanager
    def cls(self, name):
        self.indented(f"class {name}:")
        self.indent += 1
        yield
        self.indent -= 1

    def indented(self, string):
        self.file.write(self.indent_string * self.indent)
        self.file.write(string)
        self.file.write(self.newline)
        return self

    def prop(self, name, val=None, type_=None):
        string = name
        if not type_ is None:
            string += f":{type_}"
        if not val is None:
            string += f" = {val}"
        self.indented(string)
        return self
