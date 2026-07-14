__doc__ = """
NAME
    uname - display system information

SYNOPSIS
    uname()

DESCRIPTION
    Displays system information.

    Returns:
        (sysname, nodename, release, version, machine)

    Returns None on failure.
"""

import mush

sysinfo = mush._load_internal("_sys")


def main():
    try:
        info = sysinfo["uname_info"]()
    except Exception as e:
        print("uname: {}".format(e))
        return None

    print("{} {} {} {} {}".format(*info))
    return info
