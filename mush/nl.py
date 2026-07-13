__doc__ = """
NAME
    nl - number lines of files

SYNOPSIS
    nl(file1, [file2 ...], out=None, collect=False)
    nl(out=None, collect=False)

DESCRIPTION
    Prints the contents of one or more files with line numbers.

    If called without arguments, reads from standard input.

EXAMPLES
    nl("boot.py")
    nl("a.txt", "b.txt")
    nl()
"""

import sys
import mush

fsio = mush._load_internal("_fsio")


def _write_line(write, lineno, line, newline):
    write("{:6}\t".format(lineno))
    write(fsio["decode"](line))

    if newline:
        write("\n")

    return lineno + 1


def main(*paths, out=None, collect=False):
    write, close, result = fsio["output"](
        out=out,
        collect=collect,
    )

    try:
        lineno = 1

        if not paths:
            for line in sys.stdin:
                lineno = _write_line(
                    write,
                    lineno,
                    line.rstrip("\n").encode(),
                    True,
                )
            return result()

        for path in paths:
            try:
                for line, newline in fsio["iter_lines"](path):
                    lineno = _write_line(
                        write,
                        lineno,
                        line,
                        newline,
                    )
            except OSError as e:
                print("nl: {}: {}".format(path, e))

    finally:
        close()

    return result()
