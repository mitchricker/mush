__doc__ = """
NAME
    pwd - print working directory

SYNOPSIS
    pwd()

DESCRIPTION
    Prints the current working directory.

EXAMPLES
    pwd()
"""
import os
def main():
    try:
        cwd = os.getcwd()
    except OSError as e:
        print("pwd: {}".format(e))
    
    print(cwd)
    
    return cwd
