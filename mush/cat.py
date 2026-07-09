__doc__ = """
NAME
    cat - concatenate and print files

SYNOPSIS
    cat(file1, [file2 ...])

DESCRIPTION
    Streams file contents to stdout using mush filesystem kernel.
"""
import sys
import mush
fsio = mush._load_internal("_fsio")
def main(*paths):
    if not paths:
        data = sys.stdin.read()
        sys.stdout.write(data)
        return
    for path in paths:
        try:
            for chunk in fsio["read_chunks"](path):
                sys.stdout.write(
                    chunk.decode(
                        "utf-8",
                        "ignore",
                    )
                )
        except OSError as e:
            print(
                "cat: {}: {}".format(
                    path,
                    e,
                )
            )
