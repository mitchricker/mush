__doc__ = """
NAME
    cat - concatenate and print files

SYNOPSIS
    cat(file1, [file2 ...], out=None, collect=False)

DESCRIPTION
    Streams file contents using mush filesystem helpers.

    Returns:
        collect=False:
            None on success
            False on failure

        collect=True:
            file contents as bytes or string

EXAMPLES
    cat("boot.py")

    cat("image.bin", out="copy.bin")

    cat("config.txt", collect=True)
"""

import sys
import mush

fsio = mush._load_internal("_fsio")


def main(*paths, out=None, collect=False):
    write, close, result = fsio["output"](
        out=out,
        collect=collect,
    )

    success = True

    try:
        if not paths:
            try:
                data = sys.stdin.read()
                write(data)

            except Exception as e:
                print(
                    "cat: stdin: {}".format(
                        e,
                    )
                )

                return False

        for path in paths:
            try:
                for chunk in fsio["read_chunks"](path):
                    write(chunk)

            except OSError as e:
                print(
                    "cat: {}: {}".format(
                        path,
                        e,
                    )
                )

                success = False

    finally:
        close()

    if not success:
        return False

    if collect:
        return result()

    return None
