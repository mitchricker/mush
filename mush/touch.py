__doc__ = """
NAME
    touch - create empty file or update timestamp

SYNOPSIS
    touch(file1, [file2 ...], collect=False)

DESCRIPTION
    Creates empty files if they do not exist.

    If the file exists:
        Updates its modification time.

    Returns:
        collect=True:
            list of files updated

        collect=False:
            None on success
            False on failure

EXAMPLES
    touch("newfile.txt")

    touch(
        "a.txt",
        "b.txt",
    )

    touch(
        "a.txt",
        "b.txt",
        collect=True,
    )
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
        print(
            "touch: cannot create '{}': {}".format(
                path,
                e,
            )
        )

        return False


def main(*paths, collect=False):
    if not paths:
        print(
            "touch: missing file operand"
        )
        return False

    updated = []

    for path in paths:
        if not _touch_one(path):
            return False

        updated.append(path)

    if collect:
        return updated

    return None
