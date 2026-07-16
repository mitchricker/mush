__doc__ = """
NAME
    pwd - print working directory

SYNOPSIS
    pwd(collect=False)

DESCRIPTION
    Prints the current working directory.

    Returns:
        collect=True:
            current working directory

        collect=False:
            None on success
            False on failure

EXAMPLES
    pwd()

    pwd(collect=True)
"""

import os


def main(collect=False):
    try:
        cwd = os.getcwd()

        if collect:
            return cwd

        print(cwd)

        return None

    except Exception as e:
        print(
            "pwd: {}".format(e)
        )

        return False
