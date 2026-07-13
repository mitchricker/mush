__doc__ = """
NAME
    ls - list directory contents

SYNOPSIS
    ls([path="."])

DESCRIPTION
    Lists files and directories.

    Displays type, size, and name.

    Returns the number of entries displayed.

EXAMPLES
    ls()

    ls("/flash")
"""

import os


def _is_dir(mode):
    return bool(mode & 0x4000)


def _path_join(path, name):
    if path == ".":
        return name

    if path.endswith("/"):
        return path + name

    return path + "/" + name


def main(path="."):
    try:
        entries = os.listdir(path)
    except OSError as e:
        print("ls: cannot access '{}': {}".format(path, e))
        return 0

    print("{:<4} {:>10} {}".format(
        "TYPE",
        "SIZE",
        "NAME",
    ))

    for name in entries:
        full = _path_join(path, name)

        typ = "?"
        size = 0

        try:
            st = os.stat(full)

            if _is_dir(st[0]): typ = "d"
            else: typ = "-"

            size = st[6]

        except OSError:
            pass

        print("{:<4} {:>10} {}".format(
            typ,
            size,
            name,
        ))

    return entries
