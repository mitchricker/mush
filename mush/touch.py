__doc__ = """
NAME
    touch - create empty file or update timestamp

SYNOPSIS
    touch(file1, [file2 ...])

DESCRIPTION
    Creates empty files if they do not exist.
    If the file exists, updates its modification time.
"""

import os


def _touch_one(path):
    try:
        if hasattr(os, "utime"):
            os.utime(path, None)
            return True
    except Exception:
        pass

    try:
        with open(path, "a"):
            pass
        return True

    except OSError as e:
        print("touch: cannot create '{}': {}".format(path, e))
        return False


def main(*paths):
    if not paths:
        print("touch: missing file operand")
        return False

    success = True

    for path in paths:
        if not _touch_one(path):
            success = False

    return success