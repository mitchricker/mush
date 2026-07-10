__doc__ = """
NAME
    uniq - remove adjacent duplicate lines

SYNOPSIS
    uniq(file)

DESCRIPTION
    Reads a file and prints lines while removing
    consecutive duplicate lines.

EXAMPLES
    uniq("log.txt")
"""
import mush
fsio = mush._load_internal("_fsio")
def _print_line(line):
    try:
        print(line.decode("utf-8", "ignore"))
    except Exception:
        print(line)
def main(path):
    previous = None
    try:
        for line, terminated in fsio["iter_lines"](path):
            if line != previous:
                _print_line(line)
                previous = line
    except OSError as e:
        print(
            "uniq: {}: {}".format(
                path,
                e,
            )
        )
