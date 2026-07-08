__doc__ = """
NAME
    head - show first N lines

SYNOPSIS
    head(file, n=10)
"""
import mush._fsio as fsio
def main(path, n=10):
    for i, line in enumerate(fsio.iter_lines(path)):
        if i >= n:
            break
        try:
            print(line.decode(errors="ignore"))
        except Exception:
            print(line)
