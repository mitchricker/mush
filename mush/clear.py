__doc__ = """
NAME
    clear - clear the terminal screen
SYNOPSIS
    clear()
DESCRIPTION
    Clears the terminal screen using ANSI escape codes.
"""
def main():
    print("\x1b[2J\x1b[H")
