__doc__ = """
NAME
    cd - change current working directory

SYNOPSIS
    cd(path)
    cd()

DESCRIPTION
    Changes the current working directory using os.chdir().

    If called without arguments, prints the current directory.

EXAMPLES
    cd("/flash")
    cd("test")
    cd()
"""
import os
def main(path=None):
    if not path:
        print(os.getcwd())
        return
    if path == "~":
        path = "/"
    try:
        os.chdir(path)
    except OSError as e:
        print("cd: {}: {}".format(path, e))
        return
    print(os.getcwd())
