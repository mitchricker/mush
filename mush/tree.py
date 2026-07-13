__doc__ = """
NAME
    tree - display directory structure

SYNOPSIS
    tree(path, maxdepth=5, out=None, collect=False)

DESCRIPTION
    Prints a visual directory tree.

EXAMPLES
    tree("/")
    tree("/flash", maxdepth=3)
    tree("/", collect=True)
"""

import os
import mush

fsio = mush._load_internal("_fsio")


def _write_line(write, depth, name):
    if depth:
        write(("  " * depth) + name + "\n")
    else:
        write(name + "\n")


def _walk(path, depth, maxdepth, write):
    if depth > maxdepth:
        return

    try:
        entries = os.listdir(path)

    except Exception:
        return

    for entry in entries:
        full = path + "/" + entry

        try:
            mode = os.stat(full)[0]
            is_dir = (mode & 0x4000) != 0

        except Exception:
            is_dir = False

        _write_line(write, depth, entry)

        if is_dir:
            _walk(
                full,
                depth + 1,
                maxdepth,
                write,
            )


def main(path, maxdepth=5, out=None, collect=False):
    write, close, result = fsio["output"](
        out=out,
        collect=collect,
    )

    try:
        write(path + "\n")

        _walk(
            path,
            1,
            maxdepth,
            write,
        )

    except Exception as e:
        print(
            "tree: {}: {}".format(
                path,
                e,
            )
        )
        return False

    finally:
        close()

    return result()
