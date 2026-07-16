__doc__ = """
NAME
    uniq - remove adjacent duplicate lines

SYNOPSIS
    uniq(file, out=None, collect=False)

DESCRIPTION
    Reads a file and removes consecutive duplicate lines.

    Returns:

        collect=True:
            list of unique lines

        collect=False:
            None on success

        False on error

EXAMPLES
    uniq("log.txt")

    uniq(
        "log.txt",
        collect=True,
    )
"""

import mush

fsio = mush._load_internal("_fsio")


def main(
    path,
    out=None,
    collect=False,
):
    if not path:
        print(
            "uniq: missing file"
        )
        return False

    previous = None

    if collect:
        result = []

        def emit(line):
            result.append(
                fsio["decode"](line)
            )

    else:
        write, close, output_result = fsio["output"](
            out=out,
        )

        def emit(line):
            write(
                fsio["decode"](line)
            )
            write("\n")

    try:
        for line, terminated in fsio["iter_lines"](path):

            if line != previous:
                emit(line)
                previous = line

    except Exception as e:
        print(
            "uniq: {}: {}".format(
                path,
                e,
            )
        )

        return False

    finally:
        if not collect:
            close()

    if collect:
        return result

    return None
