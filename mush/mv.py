__doc__ = """
NAME
    mv - move/rename files

SYNOPSIS
    mv(src, dst)

DESCRIPTION
    Uses os.rename() when possible.
    Falls back to copy and delete.

    Returns:
        True  - success
        False - failure

EXAMPLES
    mv("a.txt", "b.txt")
"""

import os
import mush

fsio = mush._load_internal("_fsio")


def main(src, dst):
    try:
        os.rename(src, dst)

        print(
            "moved:",
            src,
            "->",
            dst,
        )

        return True

    except Exception:
        pass

    try:
        fsio["copy"](src, dst)
        os.remove(src)

        print(
            "moved:",
            src,
            "->",
            dst,
        )

        return True

    except Exception as e:
        print(
            "mv failed:",
            e,
        )

        return False
