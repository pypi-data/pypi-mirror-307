import pytest

from .conf import rm4name

ROOT, MOD = rm4name( 'describe-key-pairs.sample' )

def test_root():
    assert isinstance(ROOT, MOD.ROOT)

def test_KeyPairs():
    ROOT.KeyPairs
    ROOT['KeyPairs']
    ROOT.KeyPairs == ROOT['KeyPairs']

def test_keypair():
    keypair = ROOT.keypairs()[0]
    assert isinstance(keypair, MOD.KeyPair)
    assert repr(keypair)=="<KeyPair: tmp.bar>"



