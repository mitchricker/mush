__doc__ = """
NAME
    mkdir - create directories

SYNOPSIS
    mkdir(path)

DESCRIPTION
    Creates a directory using os.mkdir().
    Fails if parent directories do not exist.

EXAMPLES
    mkdir("data")
"""

import os


def main(path):
    try:
        os.mkdir(path)
        print("created:", path)
    except Exception as e:
        print("mkdir failed:", e)
