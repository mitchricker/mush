__doc__ = """
NAME
    find - search files in directory tree

SYNOPSIS
    find(path, name=None, contains=None, maxdepth=10)

DESCRIPTION
    Recursively searches a directory tree.

    Supports:
        - exact filename match (name)
        - substring match (contains)
        - limited recursion depth (maxdepth)

    Designed for MicroPython constraints:
        - no regex
        - no generators
        - minimal allocations
        - safe recursion depth limit

EXAMPLES
    find("/")
    find("/", name="config.json")
    find("/flash", contains=".py")
"""
import os
def _match(filename, name, contains):
    if name and filename == name:
        return True
    if contains and contains in filename:
        return True
    if not name and not contains:
        return True
    return False
def _walk(path, name, contains, depth, maxdepth):
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
        if is_dir:
            _walk(full, name, contains, depth + 1, maxdepth)
        else:
            if _match(e, name, contains):
                print(full)
def main(path, name=None, contains=None, maxdepth=10):
    _walk(path, name, contains, 0, maxdepth)
