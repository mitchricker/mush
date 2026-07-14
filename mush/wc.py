__doc__ = """
NAME
    wc - count newline, word, and byte counts

SYNOPSIS
    wc(file1, [file2 ...], collect=False)

DESCRIPTION
    Streams files using mush _fsio and computes:

        - lines
        - words
        - bytes

    Returns:
        collect=False:
            Prints results and returns counts.

        collect=True:
            Returns structured results without printing.

    Examples:
        wc("boot.py")

        wc("a.txt", "b.txt")

        wc("log.txt", collect=True)
"""

import mush

fsio = mush._load_internal("_fsio")


def _count_stream(path):
    lines = 0
    words = 0
    bytes_ = 0
    in_word = False

    for chunk in fsio["read_chunks"](path):
        bytes_ += len(chunk)

        for b in chunk:
            if b == 10:
                lines += 1

            if b in (
                32,   # space
                9,    # tab
                10,   # newline
                13,   # carriage return
            ):
                if in_word:
                    words += 1
                    in_word = False
            else:
                in_word = True

    if in_word:
        words += 1

    return (
        lines,
        words,
        bytes_,
    )


def main(*paths, collect=False):
    if not paths:
        msg = "wc: missing file operand"

        if not collect:
            print(msg)

        return None

    results = []

    total_lines = 0
    total_words = 0
    total_bytes = 0

    for path in paths:
        try:
            lines, words, bytes_ = _count_stream(path)

        except OSError as e:
            msg = "wc: {}: {}".format(
                path,
                e,
            )

            if not collect:
                print(msg)

            return None

        total_lines += lines
        total_words += words
        total_bytes += bytes_

        results.append(
            (
                path,
                lines,
                words,
                bytes_,
            )
        )

        if not collect:
            print(
                "{:>6} {:>6} {:>6} {}".format(
                    lines,
                    words,
                    bytes_,
                    path,
                )
            )

    totals = (
        total_lines,
        total_words,
        total_bytes,
    )

    if len(paths) > 1:
        if not collect:
            print(
                "{:>6} {:>6} {:>6} total".format(
                    total_lines,
                    total_words,
                    total_bytes,
                )
            )

        return (
            results,
            totals,
        )

    return (
        results[0][1],
        results[0][2],
        results[0][3],
    )
