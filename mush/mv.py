__doc__ = """
NAME
    mv - move/rename files

SYNOPSIS
    mv(src, dst, collect=False)

DESCRIPTION
    Uses os.rename() when possible.
    Falls back to copy and delete.

    Returns:
        collect=False:
            None on success
            False on failure

        collect=True:
            destination path

EXAMPLES
    mv(
        "a.txt",
        "b.txt",
    )

    mv(
        "a.txt",
        "b.txt",
        collect=True,
    )
"""

import os
import mush

fsio = mush._load_internal("_fsio")


def main(
    src,
    dst,
    collect=False,
):
    try:
        os.rename(
            src,
            dst,
        )

        print(
            "moved:",
            src,
            "->",
            dst,
        )

        return dst if collect else None

    except Exception:
        pass

    try:
        fsio["copy"](
            src,
            dst,
        )

        os.remove(src)

        print(
            "moved:",
            src,
            "->",
            dst,
        )

        return dst if collect else None

    except Exception as e:
        print(
            "mv failed:",
            e,
        )

        return False
