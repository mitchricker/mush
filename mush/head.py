__doc__ = """
NAME
    head - show first N lines

SYNOPSIS
    head(file, n=10, out=None, collect=False)

DESCRIPTION
    Prints the first N lines of a file.

EXAMPLES
    head("boot.py")
    head("log.txt", n=20)
"""

import mush

fsio = mush._load_internal("_fsio")


def main(path, n=10, out=None, collect=False):
    write, close, result = fsio["output"](
        out=out,
        collect=collect,
    )

    try:
        for i, (line, terminated) in enumerate(
            fsio["iter_lines"](path)
        ):
            if i >= n:
                break

            write(fsio["decode"](line))

            if terminated:
                write("\n")

    finally:
        close()

    return result()
