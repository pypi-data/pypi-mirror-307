#!/usr/bin/env python3

import json
import subprocess

from .util import note, bold

from .wrapping import wrap4cmd

class Profile:

    def __repr__(s):
        return f"<Profile: {s._profile}>"

    def __init__(self,profile):
        self._profile = profile

    def invoke( self, line ):
        cmd = line.split()[0]
        args = line[len(cmd):].strip()
        line = f"aws ec2 --profile {self._profile} {cmd.replace('_','-')} {args}"
        it=subprocess.run(line.split(), capture_output=True, text=True)
        return Meta(it, line, cmd)

class Meta:

    def __init__(self, it, line, cmd):
        self._it = it
        self._line = line
        self._cmd = cmd
        self.stdout = self._it.stdout
        self.stderr = self._it.stderr
        self.wrapper = wrap4cmd(cmd)
        try:    self.root = self.wrapper(json.loads(self.stdout))
        except: self.root = None

    def __bool__(self):
        return bool(self.root is not None)


    def __repr__(s):
        it=s._it
        out=s._stdout[:1000] + 'df'
        err=s._stderr.rstrip()
        if err: err=f"\n\n---- stderr {'-'*50}\n{err}"
        if out: out=f"\n\n---- stdout {'-'*50}\n{out}"
        return bold(f"""==== <Meta> {'='*60}
    cmd:  [{s._cmd}]
    exec: [{s._line}]
    code: [{it.returncode}]
    wrapper: {s.wrapper.__name__}
    root: {s.root} {err} {out}\n{'='*50}
    """)

'''

def wrap4profile4name(profile,name,args=''):
    return meta4profilername(profile,name,args='').wrapped()

def meta4profile4name(profile,name,args=''):
    wrapper = WRAPPER(name.replace('-','_'))
    it  = invoke4profile4name(profile,name,args)
    return Meta(it, wrapper)

def invoke4profile4name(profile,name,args=''):
    cmdline = f"aws ec2 --profile {profile} {name.replace('_','-')} {args}"
    it = ezrun(cmdline, show=True)
    return it
    out = it.stdout or {'STATE':'Error'}
    return json.loads(out), it

class ___INVOKER:
    def __init__(self, profile):
        self.profile = profile
    def __getattr__(self, name):
        def fn(profile, name=name):
            return WRAPPER(name)(invoke4profile4name(profile,name))
        return fn(self.profile)
'''

