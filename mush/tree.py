__doc__ = """
NAME
    tree - display directory structure

SYNOPSIS
    tree(path, maxdepth=5)

DESCRIPTION
    Prints a visual directory tree.

EXAMPLES
    tree("/")
    tree("/flash", maxdepth=3)
"""
import os
def _indent(depth):
    return "  " * depth
def _walk(path, depth, maxdepth):
    if depth > maxdepth:
        return
    try:
        entries = os.listdir(path)
    except Exception:
        return
    for e in entries:
        full = path + "/" + e
        try:
            st = os.stat(full)
            is_dir = (st[0] & 0x4000) != 0
        except Exception:
            is_dir = False
        print("{}{}".format(_indent(depth), e))
        if is_dir:
            _walk(full, depth + 1, maxdepth)
def main(path, maxdepth=5):
    print(path)
    _walk(path, 1, maxdepth)
