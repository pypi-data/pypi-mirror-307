import pytest

from .wrapping import Root, DUMMY

FOOBAR = {'foo':'bar'}
ROOT=Root(FOOBAR)

def test_dunder_repr():
    assert repr(ROOT)=='<Root>'

def test_dunder_getitem():
    ROOT['foo'] == FOOBAR['foo']

def test_method_keys():
    ROOT.keys() == FOOBAR.keys()

def test_method_items():
    assert ROOT.items() == FOOBAR.items()

def test_method_values():
    assert list(ROOT.values()) == list(FOOBAR.values())

def test_AttributeError():
    with pytest.raises(AttributeError):
        ROOT.xxx

def test_KeyError():
    with pytest.raises(KeyError):
        ROOT['xxx']

def test_DUMMY_dunder_repr():
    assert repr(DUMMY())=='<DUMMY: (just a dummy)>'
