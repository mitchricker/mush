__doc__ = """
NAME
    mkdir - create a directory

SYNOPSIS
    mkdir(path, collect=False)

DESCRIPTION
    Creates a directory.

    Returns:
        collect=True:
            created path

        collect=False:
            None on success
            False on failure

EXAMPLES
    mkdir("logs")

    mkdir(
        "logs",
        collect=True,
    )
"""

import os


def main(
    path,
    collect=False,
):
    if not path:
        print(
            "mkdir: missing path"
        )
        return False

    try:
        os.mkdir(path)

        if collect:
            return path

        print(
            "created: {}".format(
                path
            )
        )

        return None

    except Exception as e:
        print(
            "mkdir: {}".format(e)
        )

        return False
