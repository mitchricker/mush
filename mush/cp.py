__doc__ = """
NAME
    cp - copy files

SYNOPSIS
    cp(src, dst)

DESCRIPTION
    Stream-based file copy using fixed-size chunks.

EXAMPLES
    cp("a.txt", "b.txt")
"""
import mush
fsio = mush._load_internal("_fsio")
def main(src, dst):
    f = None
    try:
        f = open(dst, "wb")
        for b in fsio["read_chunks"](src):
            f.write(b)
    finally:
        if f:
            f.close()
