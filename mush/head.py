__doc__ = """
NAME
    head - show first N lines

SYNOPSIS
    head(file, n=10)

DESCRIPTION
    Prints the first N lines of a file.

EXAMPLES
    head("boot.py")
    head("log.txt", 20)
"""
import mush
fsio = mush._load_internal("_fsio")
def main(path, n=10):
    for i, (line, terminated) in enumerate(fsio["iter_lines"](path)):
        if i >= n:
            break
        try:
            print(line.decode("utf-8", "ignore"))
        except Exception:
            print(line)
