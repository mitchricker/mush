__doc__ = """
NAME
    head - show first N lines

SYNOPSIS
    head(path, n=10, out=None, collect=False)

DESCRIPTION
    Prints the first N lines of a file.

    Returns:
        collect=False:
            None on success
            False on failure

        collect=True:
            Generated text output

EXAMPLES
    head("boot.py")

    head("log.txt", n=20)

    head(
        "log.txt",
        out="first-lines.txt",
    )

    head(
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
    write, close, result = fsio["output"](
        out=out,
        collect=collect,
    )

    try:
        count = 0

        for line, terminated in fsio["iter_lines"](path):
            if count >= n:
                break

            write(
                fsio["decode"](line)
            )

            if terminated:
                write("\n")

            count += 1

    except OSError as e:
        print(
            "head: {}: {}".format(
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
