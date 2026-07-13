__doc__ = """
NAME
    mkdir - create a directory

SYNOPSIS
    mkdir(path)

DESCRIPTION
    Creates a directory.

EXAMPLES
    mkdir("logs")
"""

import os


def main(path):
    try:
        os.mkdir(path)
        print("created:", path)
        return path

    except Exception as e:
        print("mkdir failed:", e)
        return False