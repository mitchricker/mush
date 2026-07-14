__doc__ = """
NAME
    uniq - remove adjacent duplicate lines

SYNOPSIS
    uniq(file, out=None, collect=False)

DESCRIPTION
    Reads a file and removes consecutive duplicate lines.

    Returns:
        count of unique lines normally

        list of lines with collect=True

        False on error

EXAMPLES
    uniq("log.txt")

    uniq("log.txt", collect=True)
"""

import mush

fsio = mush._load_internal("_fsio")


def main(path, out=None, collect=False):
    previous = None
    count = 0

    if collect:
        result = []

        def emit(line):
            result.append(line)

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
                count += 1

    except OSError as e:
        if not collect:
            close()

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

    return count
