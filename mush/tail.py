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
    buf = []

    for line, terminated in fsio["iter_lines"](path):
        buf.append(line)

        if len(buf) > n:
            del buf[0]

    write, close, result = fsio["output"](
        out=out,
        collect=collect,
    )

    try:
        for line in buf:
            try:
                write(line.decode("utf-8", "ignore"))
            except Exception:
                write(str(line))

            write("\n")

    finally:
        close()

    return result()
