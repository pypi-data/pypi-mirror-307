import pytest

from .conf import rm4name

ROOT, MOD = rm4name( 'describe-instances.basic' )

def test_():
    return
    assert ROOT['Reservations']
    assert ROOT.Reservations
    assert ROOT.Reservations == ROOT['Reservations']
    assert 'Instances' in ROOT.Reservations[0].keys()




