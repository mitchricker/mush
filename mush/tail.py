__doc__ = """
NAME
    tail - show last N lines

SYNOPSIS
    tail(file, n=10, out=None, collect=False)

DESCRIPTION
    Prints the last N lines of a file.

    Returns:
        collect=True:
            Generated text output

        collect=False:
            None on success
            False on failure

EXAMPLES
    tail("boot.py")

    tail("log.txt", n=20)

    tail(
        "log.txt",
        out="last-lines.txt",
    )

    tail(
        "boot.py",
        collect=True,
    )
"""

import mush

fsio = mush._load_internal("_fsio")


def main(
    path,
    n=10,
    out=None,
    collect=False,
):
    if not path:
        print(
            "tail: missing file"
        )
        return False

    if n < 0:
        print(
            "tail: invalid line count"
        )
        return False

    lines = []

    try:
        for line in fsio["iter_lines_reverse"](path):
            lines.append(line)

            if len(lines) >= n:
                break

    except Exception as e:
        print(
            "tail: {}: {}".format(
                path,
                e,
            )
        )

        return False

    try:
        write, close, result = fsio["output"](
            out=out,
            collect=collect,
        )

    except Exception as e:
        print(
            "tail: {}".format(e)
        )
        return False

    try:
        while lines:
            write(
                fsio["decode"](
                    lines.pop()
                )
            )

            write("\n")

    except Exception as e:
        print(
            "tail: {}".format(e)
        )
        return False

    finally:
        close()

    if collect:
        return result()

    return None
