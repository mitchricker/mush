__doc__ = """
NAME
    uname - display system information

SYNOPSIS
    uname()

DESCRIPTION
    Displays system information.

    Returns:
        system information dictionary

    Returns None on failure.
"""

import mush

sysinfo = mush._load_internal("_sys")


def main():
    try:
        info = sysinfo["uname_info"]()

    except Exception as e:
        print(
            "uname: {}".format(e)
        )
        return None

    print(
        "{} {} {} {} {}".format(
            info.get("sysname", ""),
            info.get("nodename", ""),
            info.get("release", ""),
            info.get("version", ""),
            info.get("machine", ""),
        )
    )

    return info
