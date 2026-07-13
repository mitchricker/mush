import gc
import os
import sys

__version__ = "0.3.0"
__author__ = "Mitch Ricker"
__license__ = "MIT"
_COMMANDS = {}
_INTERNAL = {}

def _find_root():
    cwd = os.getcwd()
    for prefix in sys.path:
        if prefix == ".frozen":
            continue
        if prefix:
            path = prefix.rstrip("/") + "/mush"
        else:
            path = cwd.rstrip("/") + "/mush"
        try:
            os.listdir(path)
            return path
        except OSError:
            pass
    raise ImportError("cannot locate mush package")

_ROOT = _find_root()

parent = _ROOT.rsplit("/", 1)[0]
if parent not in sys.path:
    sys.path.append(parent)

class _Module:
    def __init__(self, values):
        self.__dict__.update(values)


def _load_internal(name):
    if name in _INTERNAL:
        return _INTERNAL[name]

    path = _ROOT + "/" + name + ".py"

    try:
        f = open(path)
        source = f.read()
        f.close()
    except Exception:
        raise ImportError(
            "mush: internal module '{}' not found".format(name)
        )

    module = {}

    exec(source, module)

    _INTERNAL[name] = module

    return module


def _load(cmd):
    if cmd in _COMMANDS:
        return _COMMANDS[cmd]

    path = _ROOT + "/" + cmd + ".py"

    try:
        f = open(path)
        source = f.read()
        f.close()
    except Exception:
        raise ImportError(
            "mush: command '{}' not found at {}".format(
                cmd,
                path,
            )
        )

    module = {
        "__name__": "mush." + cmd,
        "__file__": path,
    }

    exec(source, module)

    if "main" not in module:
        raise ImportError(
            "mush: '{}' missing main()".format(cmd)
        )

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
    for filename in os.listdir(_ROOT):
        if (
            filename.endswith(".py")
            and not filename.startswith("_")
            and filename != "__init__.py"
        ):
            command = filename[:-3]
            globals()[command] = _make(command)

except Exception as e:
    print(
        "mush: command discovery failed:",
        e,
    )


print(
    "Welcome to Mitch's Micro Shell. Run man() to get started."
)
