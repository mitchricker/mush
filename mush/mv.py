__doc__ = """
NAME
    mv - move/rename files

SYNOPSIS
    mv(src, dst)

DESCRIPTION
    Uses os.rename() when possible.
    Falls back to cp + delete.

EXAMPLES
    mv("a.txt", "b.txt")
"""
import os
import mush
fsio = mush._load_internal("_fsio")
def main(src, dst):
    try:
        os.rename(src, dst)
        return
    except Exception:
        pass
    dst_file = None
    try:
        dst_file = open(dst, "wb")
        for chunk in fsio["read_chunks"](src):
            dst_file.write(chunk)
    finally:
        if dst_file:
            dst_file.close()
    try:
        os.remove(src)
    except Exception:
        pass
