#!/usr/bin/env python3
from importlib import import_module

from .util import  warn, note

def repr4dikt(d):
    return ' '.join([ f"[{k}:{v}]" for k,v in d.items() ])

def repr4obj(obj, x):
    name = f"{obj.__class__.__name__}"
    return f"<{name}: {x}>"


class Root():
    """Encapsulate a json dictionary
    """
    def __init__(self,dikt={}):
        self._dikt = dikt

    def _repr(self):
        return ''

    def __getitem__(self,name):
        try:
            return self._dikt[name]
        except KeyError:
            raise KeyError( f"\n\n\tobj = {self}\n\n\tobj['{name}'] does not exist" )

    def __getattr__(self, name):
        try:
            return self._dikt[name]
        except KeyError:
            raise AttributeError( f"\n\n\tobj = {self}\n\n\tobj.{name} does not exist")

    def __repr__(s):
        extra = s._repr()
        extra = extra and f": {extra}"
        return f"<{s.__class__.__name__}{extra}>"

    def keys(s):   return s._dikt.keys()
    def items(s):  return s._dikt.items()
    def values(s): return s._dikt.values()


class DUMMY(Root):
    """This is the subclass of Root that is used when cmd cannot resolve."""
    def _repr(self):
        return '(just a dummy)'

def wrap4cmd(cmd):
    name = cmd.replace( '-', '_' )
    dotted = f"{__package__}.aws.ec2.{name}"
    path = dotted.replace('.','/') + '.py'
    try:
        return import_module(dotted).ROOT
    except ModuleNotFoundError:
        warn(f'Wrapper: cannot find [{path}].')
    except AttributeError:
        warn(f'Wrapper: cannot load [{path}].')
    return DUMMY

