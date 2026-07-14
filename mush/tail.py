__doc__ = """
NAME
    tail - show last N lines

SYNOPSIS
    tail(file, n=10, out=None, collect=False)

DESCRIPTION
    Prints the last N lines of a file.

EXAMPLES
    tail("boot.py")
    tail("log.txt", n=20)
"""

import mush

fsio = mush._load_internal("_fsio")


def main(path, n=10, out=None, collect=False):
    lines = []

    for line in fsio["iter_lines_reverse"](path):
        lines.append(line)

        if len(lines) >= n:
            break

    write, close, result = fsio["output"](
        out=out,
        collect=collect,
    )

    try:
        while lines:
            write(fsio["decode"](lines.pop()))
            write("\n")

    finally:
        close()

    return result()
