__doc__ = """
NAME
    grep - search text for a pattern

SYNOPSIS
    grep(pattern, path, [path2 ...], ignore_case=False,
         out=None, collect=False)

DESCRIPTION
    Searches files for lines matching a regular expression.

    Returns:

        collect=True:
            list of tuples:

            (
                path,
                line_number,
                text
            )

        collect=False:
            None on success

        False on error

EXAMPLES
    grep(
        "wifi",
        "boot.py",
    )

    grep(
        "^import",
        "main.py",
    )

    grep(
        "warning",
        "log.txt",
        ignore_case=True,
    )

    grep(
        "TODO",
        "src.py",
        collect=True,
    )
"""

import re
import mush

fsio = mush._load_internal("_fsio")


def main(
    pattern,
    *paths,
    ignore_case=False,
    out=None,
    collect=False,
):
    if not paths:
        print(
            "grep: missing file operand"
        )
        return False

    flags = 0

    if ignore_case:
        flags |= re.IGNORECASE

    try:
        regex = re.compile(
            pattern,
            flags,
        )

    except Exception as e:
        print(
            "grep: invalid pattern: {}".format(e)
        )
        return False

    if collect:
        matches = []

        def emit(path, lineno, text):
            matches.append(
                (
                    path,
                    lineno,
                    text,
                )
            )

        close = None

    else:
        write, close, result = fsio["output"](
            out=out,
        )

        def emit(path, lineno, text):
            write(
                "{}:{}:{}".format(
                    path,
                    lineno,
                    text,
                )
            )
            write("\n")

    try:
        for path in paths:
            try:
                for lineno, item in enumerate(
                    fsio["iter_lines"](path),
                    1,
                ):
                    line, newline = item

                    text = fsio["decode"](line)

                    if regex.search(text):
                        emit(
                            path,
                            lineno,
                            text,
                        )

            except OSError as e:
                print(
                    "grep: {}: {}".format(
                        path,
                        e,
                    )
                )

                return False

    finally:
        if close:
            close()

    if collect:
        return matches

    return None
