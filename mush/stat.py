__doc__ = """
NAME
    stat - file metadata information

SYNOPSIS
    stat(path)

DESCRIPTION
    Displays file or directory metadata using os.stat().

    Returns:
        (
            path,
            size_bytes,
            mode,
            type,
        )

    Fields are MicroPython-dependent.

EXAMPLES
    stat("file.txt")
"""

import os
import mush

sys = mush._load_internal("_sys")


def main(path):
    try:
        s = os.stat(path)

        size = s[6]
        mode = s[0]

        if mode & 0x4000:
            file_type = "directory"
        else:
            file_type = "file"

        print("STAT: {}".format(path))
        print("  size : {}".format(
            sys["format_size"](size)
        ))
        print("  mode : {}".format(mode))
        print("  type : {}".format(file_type))

        return (
            path,
            size,
            mode,
            file_type,
        )

    except Exception as e:
        print("stat failed:", e)
        return None
