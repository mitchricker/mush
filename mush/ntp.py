__doc__ = """
NAME
    ntp - synchronize clock using Network Time Protocol

SYNOPSIS
    ntp()
    ntp(server)

DESCRIPTION
    Synchronizes the system clock using SNTP.

    Requires an active network connection.

    Default server:
        pool.ntp.org

    Options:
        server:
            NTP server hostname.

    Returns:
        True    - clock synchronized successfully
        False   - synchronization failed

EXAMPLES
    ntp()

    ntp(
        "time.google.com",
    )
"""

import machine
import mush

_ntp = mush._load_internal("_ntp")


def main(server=_ntp["DEFAULT_SERVER"]):
    if not server:
        print(
            "ntp: missing server"
        )
        return False

    try:
        print(
            "ntp: contacting {}".format(
                server
            )
        )

        _ntp["sync"](server)

        t = machine.RTC().datetime()

        print(
            "time set: {:04d}-{:02d}-{:02d} "
            "{:02d}:{:02d}:{:02d}".format(
                t[0],
                t[1],
                t[2],
                t[4],
                t[5],
                t[6],
            )
        )

        return True

    except Exception as e:
        print(
            "ntp:",
            e,
        )

        return False
