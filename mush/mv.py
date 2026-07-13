__doc__ = """
NAME
    mv - move/rename files

SYNOPSIS
    mv(src, dst)

DESCRIPTION
    Uses os.rename() when possible.
    Falls back to copy and delete.

EXAMPLES
    mv("a.txt", "b.txt")
"""

import os
import mush

fsio = mush._load_internal("_fsio")


def main(src, dst):
    try:
        os.rename(src, dst)
        print("moved:", src, "->", dst)
        return True

    except Exception:
        pass

    f = None

    try:
        f = open(dst, "wb")

        for chunk in fsio["read_chunks"](src):
            f.write(chunk)

        f.close()
        f = None

        os.remove(src)

        print("moved:", src, "->" , dst)
        return dst

    except Exception as e:
        print("mv failed:", e)
        return False

    finally:
        if dst_file:
            dst_file.close()
        os.remove(src)

        print("moved:", src, "->", dst)
        return True

    except Exception as e:
        print("mv failed:", e)
        return False

    finally:
        if f:
            f.close()
