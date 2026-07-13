__doc__ = """
NAME
    tac - concatenate and print files in reverse

SYNOPSIS
    tac(file, out=None, collect=False)

DESCRIPTION
    Prints file lines in reverse order.

EXAMPLES
    tac("log.txt")
    tac("log.txt", collect=True)
"""

import mush

fsio = mush._load_internal("_fsio")


def main(path, out=None, collect=False):
    write, close, result = fsio["output"](
        out=out,
        collect=collect,
    )

    try:
        for line in fsio["iter_lines_reverse"](path):
            write(fsio["decode"](line))
            write("\n")
    except OSError as e:
        print("tac: {}: {}".format(path, e))
        return False
    finally:
        close()

    return result()
