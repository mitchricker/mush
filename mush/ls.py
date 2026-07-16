__doc__ = """
NAME
    ls - list directory contents

SYNOPSIS
    ls(path=".", collect=False)

DESCRIPTION
    Lists files and directories.

    Displays type, size, and name.

    Returns:

        collect=True:
            list of entry tuples:

            (
                name,
                type,
                size
            )

        collect=False:
            None on success
            False on error

EXAMPLES
    ls()

    ls("/flash")

    ls(
        "/flash",
        collect=True,
    )
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


def main(path=".", collect=False):
    try:
        entries = os.listdir(path)

    except OSError as e:
        print(
            "ls: cannot access '{}': {}".format(
                path,
                e,
            )
        )

        return False

    results = []

    for name in entries:
        full = _path_join(
            path,
            name,
        )

        typ = "?"
        size = 0

        try:
            st = os.stat(full)

            if _is_dir(st[0]):
                typ = "d"
            else:
                typ = "-"

            size = st[6]

        except OSError:
            pass

        results.append(
            (
                name,
                typ,
                size,
            )
        )

    if collect:
        return results

    print(
        "{:<4} {:>10} {}".format(
            "TYPE",
            "SIZE",
            "NAME",
        )
    )

    for name, typ, size in results:
        print(
            "{:<4} {:>10} {}".format(
                typ,
                size,
                name,
            )
        )

    return None
