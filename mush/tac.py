__doc__ = """
NAME
    tac - concatenate and print files in reverse

SYNOPSIS
    tac(file, out=None, collect=False)

DESCRIPTION
    Prints file lines in reverse order.

    Returns:
        collect=False:
            None on success
            False on failure

        collect=True:
            Reversed file contents

EXAMPLES
    tac("log.txt")

    tac("log.txt", collect=True)

    tac("log.txt", out="reversed.txt")
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
        print(
            "tac: {}: {}".format(
                path,
                e,
            )
        )

        return False

    finally:
        close()

    if collect:
        return result()

    return None
