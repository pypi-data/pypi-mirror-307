#!/usr/bin/env python3
from bh_aws_wrap import Root

def repr4dikt(d):
    return ' '.join([ f"[{k}:{v}]" for k,v in d.items() ])

def repr4obj(obj, x):
    name = f"{obj.__class__.__name__}"
    return f"<{name}: {x}>"

class DESCRIBE_INSTANCES(Root):
    def __init__(self,*a,**b):
        Root.__init__(self,*a,**b)
    def reservations(self):
        return [Reservation(x) for x in self.Reservations]
    def compile_instances(self):
        for res in self.reservations():
            for inst in res.instances():
                yield inst
    def compile_names(self):
        for inst in self.compile_instances():
            try:
                yield inst.tags()['Name']
            except KeyError:
                continue


class Reservation(Root):
    def instances(self):
        return [Instance(x) for x in self['Instances']]


class wrapTags(Root):
    def _repr(self):
        return repr4dikt(self._dikt)

class Tag(Root):
    def _repr(self):
        return f"{self.Key}:{self.Value}"

class Instance(Root):
    def _repr(self):
        return f"[Name:{self.name()}]"
    def tags(self):
        return [ Tags(x) for x in Tags ]
    def my_Tags(self):
        aa = [Tag(x) for x in self.Tags]
        bb = { tag.Key : tag.Value for tag in aa }
        return wrapTags(bb)
    def name(self):
        return self.my_Tags().Name

ROOT=DESCRIBE_INSTANCES
