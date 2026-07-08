__doc__ = """
NAME
    date - display the current date and time

SYNOPSIS
    date()

DESCRIPTION
    Prints the current local date and time.

EXAMPLES
    date()
"""

import time

def main():
    try:
        t = time.localtime()
        print(
            "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
                t[0], t[1], t[2],
                t[3], t[4], t[5]
            )
        )
    except Exception as e:
        print("date: {}".format(e))