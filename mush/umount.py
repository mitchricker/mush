__doc__ = """
NAME
    umount - unmount a filesystem

SYNOPSIS
    umount(path)

DESCRIPTION
    Unmounts a mounted filesystem using os.umount().

    Returns:
        True  - success
        False - failure

EXAMPLES
    umount("/sd")
"""

import os


def main(path):
    if not path:
        print(
            "umount: missing path"
        )
        return False

    try:
        os.umount(path)

        print(
            "unmounted {}".format(
                path
            )
        )

        return True

    except OSError as e:
        print(
            "umount: {}: {}".format(
                path,
                e,
            )
        )

        return False
