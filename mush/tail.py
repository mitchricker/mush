__doc__ = """
NAME
    tail - show last N lines

SYNOPSIS
    tail(file, n=10)
"""
import mush
fsio = mush._load_internal("_fsio")
def main(path, n=10):
    buf = []
    for line in fsio["iter_lines"](path):
        buf.append(line)
        if len(buf) > n:
            buf.pop(0)
    for line in buf:
        try:
            print(line.decode(errors="ignore"))
        except Exception:
            print(line)
