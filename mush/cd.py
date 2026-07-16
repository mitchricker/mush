__doc__ = """
NAME
    cd - change current working directory

SYNOPSIS
    cd(path=None, collect=False)

DESCRIPTION
    Changes the current working directory.

    If called without a path, displays the current
    working directory.

    "~" is treated as the filesystem root ("/").

    Returns:
        collect=True:
            current working directory

        collect=False:
            None on success
            False on failure

EXAMPLES
    cd("/flash")

    cd("test")

    cd()

    cd(
        "/flash",
        collect=True,
    )
"""

import os


def main(
    path=None,
    collect=False,
):
    try:
        if path:
            if path == "~":
                path = "/"

            os.chdir(path)

        cwd = os.getcwd()

        if collect:
            return cwd

        print(cwd)

        return None

    except Exception as e:
        print(
            "cd: {}: {}".format(
                path,
                e,
            )
        )

        return False
