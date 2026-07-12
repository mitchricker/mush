__doc__ = """
NAME
    umount - unmount a filesystem

SYNOPSIS
    umount(path)

DESCRIPTION
    Unmounts a mounted filesystem.

EXAMPLES
    umount("/sd")
"""
import os
def main(path):
    try:
        os.umount(path)
        print("unmounted {}".format(path))
    except OSError as e:
        print("umount: {}: {}".format(path, e))
