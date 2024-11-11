from pathlib import Path
import pytest
import json

from importlib import import_module
from bh_aws_wrap.wrapping import wrap4cmd
from bh_aws_wrap.util import note
PACKAGE='bh_aws_wrap'

SAMPLES_ROOT=Path(__file__).parent/'aws.samples'

note(SAMPLES_ROOT)
assert SAMPLES_ROOT.is_dir()

class Sample:
    @staticmethod
    def json4path(path):
        with open(path) as fd:
            return json.load(fd)

    def __init__(self,name):
        self._name = name
        self._path = SAMPLES_ROOT/name
        self._cmd = name.split('.')[0].replace('-','_')
        self._wrapper = wrap4cmd(self._cmd)
        self._root = self._wrapper(self.json4path(self._path))
        self.root = self._root
        self.mod = import_module( f'{PACKAGE}.aws.ec2.{self._cmd}' )
class Sample4Name(dict):
    def __call__(self, name):
        if not name in self:
            self[name] = Sample(name)
        return self[name]


@pytest.fixture(scope='session', autouse=True)
def sample4name():
    return  Sample4Name()

def rm4name(name):
    sample=Sample4Name()(name)
    return sample.root, sample.mod

@pytest.fixture(scope='session', autouse=True)
def root_mod4name():
    def fn(name):
        sample = sample4name(name)
        return sample.root, sample.mod
    return fn

