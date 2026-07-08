__doc__ = """
NAME
    ls - list directory contents

SYNOPSIS
    ls(path)

DESCRIPTION
    Lists directory contents showing:
      TYPE  SIZE(B)  NAME
    TYPE is:
      d  directory
      -  file
      
EXAMPLES
    ls()
    ls("/flash")
"""
import os
def main(path="."):
    try:
        entries = sorted(os.listdir(path))
    except OSError as e:
        print("ls: cannot access '{}': {}".format(path, e))
        return
    print("{:<4} {:>10} {}".format("TYPE", "SIZE", "NAME"))
    for name in entries:
        full = path.rstrip("/") + "/" + name if path != "." else name
        try:
            st = os.stat(full)
            mode = st[0]
            size = st[6]
            is_dir = bool(mode & 0x4000)
            typ = "d" if is_dir else "-"
        except OSError:
            typ = "?"
            size = 0
        print("{:<4} {:>10} {}".format(typ, size, name))
