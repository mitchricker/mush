__doc__ = """
NAME
    date - display the current date and time

SYNOPSIS
    date(collect=False)

DESCRIPTION
    Prints the current local date and time.

    Returns:
        collect=False:
            None on success.

        collect=True:
            Formatted date/time string.

        False on failure.

EXAMPLES
    date()

    date(
        collect=True,
    )
"""

import time


def main(collect=False):
    try:
        t = time.localtime()

        value = (
            "{:04d}-{:02d}-{:02d} "
            "{:02d}:{:02d}:{:02d}"
        ).format(
            t[0],
            t[1],
            t[2],
            t[3],
            t[4],
            t[5],
        )

        if collect:
            return value

        print(value)

        return None

    except Exception as e:
        print(
            "date: {}".format(e)
        )

        return False
