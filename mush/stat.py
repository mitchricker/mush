__doc__ = """
NAME
    stat - file metadata information

SYNOPSIS
    stat(path)

DESCRIPTION
    Displays file or directory metadata using os.stat().

    Fields are MicroPython-dependent.

EXAMPLES
    stat("file.txt")
"""
import os
def main(path):
    try:
        s = os.stat(path)
        print("STAT:", path)
        print("  size : {}".format(s[6]))
        # file type bits (best effort)
        mode = s[0]
        print("  mode : {}".format(mode))
        if mode & 0x4000:
            print("  type : directory")
        else:
            print("  type : file")
    except Exception as e:
        print("stat failed:", e)
