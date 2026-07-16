__doc__ = """
NAME
    stat - file metadata information

SYNOPSIS
    stat(path, collect=False)

DESCRIPTION
    Displays file or directory metadata using os.stat().

    Returns:
        collect=True:
            (
                path,
                size_bytes,
                mode,
                type,
            )

            type:
                "file" or "directory"

        collect=False:
            None on success
            False on failure

    Fields are MicroPython-dependent.

EXAMPLES
    stat("file.txt")

    stat(
        "file.txt",
        collect=True,
    )
"""

import os
import mush

sys = mush._load_internal("_sys")


def main(
    path,
    collect=False,
):
    if not path:
        print(
            "stat: missing path"
        )
        return False

    try:
        s = os.stat(path)

        size = s[6]
        mode = s[0]

        if mode & 0x4000:
            file_type = "directory"
        else:
            file_type = "file"

        result = (
            path,
            size,
            mode,
            file_type,
        )

        if collect:
            return result

        print(
            "STAT: {}".format(
                path
            )
        )

        print(
            "  size : {}".format(
                sys["format_size"](size)
            )
        )

        print(
            "  mode : {}".format(
                mode
            )
        )

        print(
            "  type : {}".format(
                file_type
            )
        )

        return None

    except Exception as e:
        print(
            "stat: {}: {}".format(
                path,
                e,
            )
        )

        return False
