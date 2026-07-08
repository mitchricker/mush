__doc__ = """
NAME
    touch - create empty file or update timestamp
SYNOPSIS
    touch file1 [file2 ...]
DESCRIPTION
    Creates empty files if they do not exist.
    If the file exists, updates its modification time.
"""

import os

def _touch_one(path):
    try:
        if hasattr(os, "utime"):
            os.utime(path, None)
            return
    except Exception:
        pass

    try:
        f = open(path, "a")
        f.close()
    except Exception as e:
        print("touch: cannot create '{}': {}".format(path, e))

def main(*paths):
    if not paths:
        print("touch: missing file operand")
        return

    for p in paths:
        _touch_one(p)