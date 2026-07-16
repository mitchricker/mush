__doc__ = """
NAME
    uname - display system information

SYNOPSIS
    uname(collect=False)

DESCRIPTION
    Displays system information.

    Returns:

        collect=True:
            (
                sysname,
                nodename,
                release,
                version,
                machine,
            )

        collect=False:
            None on success

        False on error

EXAMPLES
    uname()

    uname(
        collect=True,
    )
"""

import mush

sysinfo = mush._load_internal("_sys")


def main(collect=False):
    try:
        info = sysinfo["uname_info"]()

    except Exception as e:
        print(
            "uname: {}".format(e)
        )
        return False

    if collect:
        return info

    print(
        "{} {} {} {} {}".format(
            *info
        )
    )

    return None
