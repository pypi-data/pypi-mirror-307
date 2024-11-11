from pathlib import Path
import json
import pytest
from util import note
from awscli.wrapping import Wrapper
from awscli.aws.ec2.describe_key_pairs import DESCRIBE_KEY_PAIRS
from awscli.aws.ec2.describe_instances import DESCRIBE_INSTANCES
from awscli.aws.ec2.DUMMY              import DUMMY
from awscli import Wrap

testout = Path(__file__).parent/'test_output'
assert testout.is_dir()

def wrap4pth(pth):
    cmd=pth.name.split('.')[0]
    wrapper = Wrapper()(cmd)
    with open(pth) as fd:
        wrap = wrapper(json.load(fd))
    return wrap

def test_DESCRIBE_INSTANCES():
    out=testout/'describe_instances.basic'
    wrap = wrap4pth( out )
    assert wrap['Reservations']
    assert wrap.Reservations
    assert wrap.Reservations == wrap['Reservations']
    print( [x.keys() for x in wrap.Reservations] )
def test_Wrap_repr():
    assert repr(Wrap())=='<Wrap>'

def test_Wrap_subclass_repr():
    class Foo(Wrap): pass
    assert repr(Foo())=='<Foo>'

def test_Wrap_respects_basic_dictionary_methods():
    sample = {'foo':'bar'}
    wrap = Wrap( sample )
    assert wrap['foo'] == sample['foo']
    assert wrap.keys() == sample.keys()
    assert wrap.items() == sample.items()
    assert list(wrap.values()) == list(sample.values())

def test_implemented():
    """Test implemented
    """
    assert Wrapper()('describe_key_pairs') == DESCRIBE_KEY_PAIRS


def test_unimplemented():
    """Test implemented
    """
    assert Wrapper()('not_an_implemented_command') == DUMMY



