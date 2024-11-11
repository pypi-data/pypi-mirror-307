import sys

def bold(text):
    RED='\x1b[31m'
    BRIGHT='\x1b[1m'
    RESET_ALL='\x1b[0m'
    return BRIGHT + RED + text + RESET_ALL

def stdout(txt):
    sys.stdout.write(str(txt) + '\n')
    sys.stdout.flush()

def stderr(txt):
    sys.stderr.write(str(txt) + '\n')
    sys.stderr.flush()

def note(*a):
    txt = ' : '.join(map(str,a))
    stderr(bold('\n' + txt))

def warn(obj):
    note( f"warning: {obj}" )

def abort(txt):
    exit(bold(f"Aborting: {txt}"))

