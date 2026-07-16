__doc__ = """
NAME
    find - search files in directory tree

SYNOPSIS
    find(path, name=None, contains=None, maxdepth=10,
         out=None, collect=False)

DESCRIPTION
    Recursively searches a directory tree.

    Supports:
        - exact filename match (name)
        - substring match (contains)
        - limited recursion depth (maxdepth)

    Returns:
        collect=True:
            list of matching paths

        collect=False:
            None on success

        False on error

EXAMPLES
    find("/")

    find(
        "/flash",
        name="config.json",
    )

    find(
        "/flash",
        contains=".py",
    )

    find(
        "/",
        collect=True,
    )
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


def _walk(
    path,
    name,
    contains,
    depth,
    maxdepth,
    emit,
):
    if depth > maxdepth:
        return

    for entry in os.listdir(path):
        full = _join(
            path,
            entry,
        )

        try:
            mode = os.stat(full)[0]
            is_dir = (
                mode & 0x4000
            ) != 0

        except Exception:
            is_dir = False

        if is_dir:
            _walk(
                full,
                name,
                contains,
                depth + 1,
                maxdepth,
                emit,
            )

        elif _match(
            entry,
            name,
            contains,
        ):
            emit(full)


def main(
    path,
    name=None,
    contains=None,
    maxdepth=10,
    out=None,
    collect=False,
):
    if not path:
        print(
            "find: missing path"
        )

        return False

    matches = []

    if collect:

        def emit(value):
            matches.append(value)

    else:
        write, close, result = fsio["output"](
            out=out,
        )

        def emit(value):
            write(value)
            write("\n")

    try:
        _walk(
            path,
            name,
            contains,
            0,
            maxdepth,
            emit,
        )

    except Exception as e:
        print(
            "find: {}".format(e)
        )

        return False

    finally:
        if not collect:
            close()

    if collect:
        return matches

    return None
