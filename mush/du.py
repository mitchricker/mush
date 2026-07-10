__doc__ = """
NAME
    du - estimate file and directory space usage

SYNOPSIS
    du([path ...], human=False, summary=False)

DESCRIPTION
    Displays disk usage for files and directories.

    Sizes are shown in bytes by default. Use human=True for
    human-readable sizes.

EXAMPLES
    du("/")

    du("/logs", human=True)

    du("/config", summary=True)
"""
import os
import mush
sysinfo = mush._load_internal("_sys")
def _is_dir(path):
    try:
        return (os.stat(path)[0] & 0x4000) != 0
    except Exception:
        return False
def _join(a, b):
    if a.endswith("/"):
        return a + b
    return a + "/" + b
def _size(path):
    try:
        st = os.stat(path)
    except OSError as e:
        print("du: {}: {}".format(path, e))
        return 0
    if not _is_dir(path):
        return st[6]
    total = 0
    try:
        for name in os.listdir(path):
            total += _size(_join(path, name))
    except OSError as e:
        print("du: {}: {}".format(path, e))
    return total
def _print_usage(size, path, human):
    if human:
        size = sysinfo["format_size"](size)
    else:
        size = str(size)
    print("{}\t{}".format(size, path))
def _du(path, human=False, summary=False):
    total = _size(path)
    if summary:
        _print_usage(total, path, human)
        return
    if _is_dir(path):
        try:
            for name in os.listdir(path):
                child = _join(path, name)
                if _is_dir(child):
                    _du(child, human, False)
        except OSError as e:
            print("du: {}: {}".format(path, e))
    _print_usage(total, path, human)
def main(*paths, **kwargs):
    if not paths:
        paths = (".",)
    human = kwargs.get("human", False)
    summary = kwargs.get("summary", False)
    for path in paths:
        _du(path, human, summary)
