from . import interp
import io
import typing

__all__ = ['load', 'loads', 'load_file']

def load(stream: typing.TextIO, name: str = "<unknown>", vars: dict[str, typing.Any] = {}):
    i = interp.Interp(stream, name)
    i.update(vars)
    return i.run()

def loads(src: str, name: str = "<string>", vars: dict[str, typing.Any] = {}):
    with io.StringIO(src) as stream:
        return load(stream, name, vars)
    
def load_file(path: str, vars: dict[str, typing.Any] = {}):
    with open(path, 'r') as fl:
        return load(fl, path, vars)