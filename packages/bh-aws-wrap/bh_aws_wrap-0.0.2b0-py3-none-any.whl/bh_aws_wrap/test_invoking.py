import pytest
import time
import subprocess

from .aws.ec2.create_key_pair import CREATE_KEY_PAIR
from .invoking import Profile
from .invoking import Meta
from .wrapping import DUMMY

KEYNAME=f'tmp.{time.time()}'
PROFILE='showme'

@pytest.mark.slow
def test_profile():
    """Test instantiation of a Profile object.

    A Profile object wraps an AWS CLI user profile and
    can be used to invoke AWS CLI calls using the profile.


    Use:
        Profile( 'bozo' ).invoke( 'CMD [ARGS]')
            -> a Meta object
    This invokes:
        subprocess.run( 'aws ecw --profile bozo CMD [ARGS])
            -> a CompletedProcess object

    The Meta object:
        (1) wraps the CompleteProcess object.
        (2) provides the resulting stdout and stderr as strings
        (3) evaluates stdout as a json tree and wrapes that.
    """
    profile = Profile('bozo')
    assert repr(profile) == "<Profile: bozo>"

@pytest.mark.slow
def test_meta():
    """Test aspects of AWS CLI invokation via Profile

    This test costs time, so we test several aspects of
    the invokation in one test rather than factor them
    into several tests.
    """
    # A Profile object wraps the name of an AWS CLI user profile
    profile=Profile( PROFILE )

    # Profile invokes an AWS CLI call (via subprocess.run) and returns a Meta
    meta = profile.invoke( f'create-key-pair --key-name {KEYNAME}' )

    # Meta wraps the CompletedProcess object of the result of the invokation
    it = meta._it
    assert it.__class__ == subprocess.CompletedProcess

    # It should be sucessful
    assert it.returncode == 0

    # meta provides the stdout and stderr as strings.
    assert meta.stdout == it.stdout
    assert meta.stderr == it.stderr

    # stdout should be text representing a json output -- a dictionary.
    result = eval(meta.stdout)
    assert type(result) == dict
    assert eval(meta.stdout)['KeyMaterial'].startswith("-----BEGIN RSA PRIVATE KEY-----")

    assert meta.wrapper         == CREATE_KEY_PAIR
    assert meta.root.__class__  == CREATE_KEY_PAIR

    # Cleanup the junk keypair created above.
    meta = profile.invoke( f'delete-key-pair --key-name {KEYNAME}' )
    assert meta._it.returncode == 0

    meta = profile.invoke( f'describe-instances' )
    #print(meta)

