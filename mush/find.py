__doc__ = """
NAME
    find - search files in directory tree

SYNOPSIS
    find(path, name=None, contains=None, maxdepth=10, out=None, collect=False)

DESCRIPTION
    Recursively searches a directory tree.

    Supports:
        - exact filename match (name)
        - substring match (contains)
        - limited recursion depth (maxdepth)

    Returns:
        - count of matches normally
        - list of matches with collect=True
        - False on error

EXAMPLES
    find("/")

    find("/", name="config.json")

    find("/flash", contains=".py")

    find("/", collect=True)
"""

import os
import mush

fsio = mush._load_internal("_fsio")


def _match(filename, name, contains):
    if name and filename == name:
        return True

    if contains and contains in filename:
        return True

    if not name and not contains:
        return True

    return False


def _join(path, name):
    if path.endswith("/"):
        return path + name

    return path + "/" + name


def _walk(path, name, contains, depth, maxdepth, emit):
    if depth > maxdepth:
        return 0

    count = 0

    try:
        entries = os.listdir(path)

    except Exception:
        return 0

    for entry in entries:
        full = _join(path, entry)

        try:
            mode = os.stat(full)[0]
            is_dir = (mode & 0x4000) != 0

        except Exception:
            is_dir = False

        if is_dir:
            count += _walk(
                full,
                name,
                contains,
                depth + 1,
                maxdepth,
                emit,
            )

        elif _match(entry, name, contains):
            emit(full)
            count += 1

    return count


def main(
    path,
    name=None,
    contains=None,
    maxdepth=10,
    out=None,
    collect=False,
):
    matches = []

    if collect:
        def emit(value):
            matches.append(value)

    else:
        write, close, result = fsio["output"](out=out)

        def emit(value):
            write(value + "\n")

    try:
        count = _walk(
            path,
            name,
            contains,
            0,
            maxdepth,
            emit,
        )

    except Exception as e:
        if not collect:
            close()

        print("find: {}".format(e))
        return False

    finally:
        if not collect:
            close()

    if collect:
        return matches

    return count
