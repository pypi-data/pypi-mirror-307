Wrap aws ec2 commands.

<PACKAGE> = "bh_aws"
The following is a rough description. For a canonical
overview of use, consult the unit tests under [./src].

Users instantiate the class Profile with an aws cli
profile name:

    >>> profile = Profile('bozo')

Users invoke aws ec2 commands as such:

    >>> meta = profile.invoke('create-key --key-name foo')

The invokation invokes an aws invokation:

    subprocess.run( 'aws ec2 create-key --key-name foo --profile bozo'.split() )

The object [meta], an instance of class [Meta], encapsulates
the resulting subprocess.CompletedProcess object, and wraps
the stdout (if any) in the class [CREATE_KEY]

    >>> import <PACKAGE>.aws.ec2.create_key as mod
    >>> root = meta._root
    >>> assert root.__class__ = mod.CREATE_KEY
    >>> assert root.__class__ = mod.ROOT

The object [root] provides access to the json decoded output.

