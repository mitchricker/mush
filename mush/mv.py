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
import mush._fsio as fsio
def main(src, dst):
    try:
        os.rename(src, dst)
        return
    except Exception:
        pass
    # fallback
    f = None
    try:
        f = open(dst, "wb")
        for b in fsio.read_chunks(src):
            f.write(b)
    finally:
        if f:
            f.close()
    try:
        os.remove(src)
    except Exception:
        pass
