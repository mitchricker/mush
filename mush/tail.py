__doc__ = """
NAME
    tail - show last N lines

SYNOPSIS
    tail(file, n=10)

DESCRIPTION
    Prints the last N lines of a file.

EXAMPLES
    tail("boot.py")
    tail("log.txt", 20)
"""
import mush
fsio = mush._load_internal("_fsio")
def main(path, n=10):
    buf = []
    for line, terminated in fsio["iter_lines"](path):
        buf.append(line)
        if len(buf) > n:
            buf.pop(0)
    for line in buf:
        try:
            print(line.decode("utf-8", "ignore"))
        except Exception:
            print(line)
