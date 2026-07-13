__doc__="""
NAME
    nl - number lines of files

SYNOPSIS
    nl(file1,[file2 ...])
    nl()

DESCRIPTION
    Prints the contents of one or more files with line numbers.

    If called without arguments, reads from standard input.

EXAMPLES
    nl("boot.py")
    nl("a.txt","b.txt")
    nl()
"""
import sys
import mush
fsio=mush._load_internal("_fsio")
def _print_line(lineno, line, newline):
    sys.stdout.write("{:6}\t".format(lineno))
    sys.stdout.write(line.decode("utf-8","ignore"))
    if newline:
        sys.stdout.write("\n")
    return lineno+1
def main(*paths):
    lineno=1
    if not paths:
        for line in sys.stdin:
            lineno=_print_line(
                lineno,
                line.rstrip("\n").encode(),
                True,
            )
        return
    for path in paths:
        try:
            for line,newline in fsio["iter_lines"](path):
                lineno=_print_line(lineno, line, newline)
        except OSError as e:
            print("nl: {}: {}".format(path, e))
