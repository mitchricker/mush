import gc
import sys
import os

_COMMANDS = {}

def _load(cmd):
    if cmd in _COMMANDS:
        return _COMMANDS[cmd]

    path = "/mush/" + cmd + ".py"

    try:
        f = open(path)
        source = f.read()
        f.close()
    except Exception as e:
        raise ImportError("mush: command '{}' not found at {}".format(cmd, path))

    # create isolated module namespace
    module = {}

    # execute module safely
    exec(source, module)

    if "main" not in module:
        raise ImportError("mush: '{}' missing main()".format(cmd))

    fn = module["main"]

    _COMMANDS[cmd] = fn
    return fn

def _run(cmd, *args, **kwargs):
    fn = _load(cmd)
    try:
        return fn(*args, **kwargs)
    finally:
        gc.collect()

def _make(cmd):
    def fn(*args, **kwargs):
        return _run(cmd, *args, **kwargs)
    return fn

def __getattr__(name):
    if name.startswith("_"):
        raise AttributeError(name)
    return _make(name)

try:
    for f in os.listdir("/mush"):
        if f.endswith(".py") and not f.startswith("_"):
            cmd = f[:-3]
            globals()[cmd] = _make(cmd)
except:
    pass

print("Welcome to Mitch's Micro Shell. Run man() to get started.")