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

        collect=True:

            single file:
                (
                    lines,
                    words,
                    bytes,
                )

            multiple files:
                (
                    results,
                    totals,
                )

                results:
                    (
                        path,
                        lines,
                        words,
                        bytes,
                    )

                totals:
                    (
                        lines,
                        words,
                        bytes,
                    )

        collect=False:
            None on success

        False on error

EXAMPLES
    wc("boot.py")

    wc(
        "a.txt",
        "b.txt",
    )

    wc(
        "log.txt",
        collect=True,
    )
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
                32,
                9,
                10,
                13,
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
        print(
            "wc: missing file operand"
        )
        return False

    results = []

    total_lines = 0
    total_words = 0
    total_bytes = 0

    for path in paths:
        try:
            lines, words, bytes_ = _count_stream(path)

        except Exception as e:
            print(
                "wc: {}: {}".format(
                    path,
                    e,
                )
            )
            return False

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

    totals = (
        total_lines,
        total_words,
        total_bytes,
    )

    if collect:
        if len(paths) == 1:
            return (
                results[0][1],
                results[0][2],
                results[0][3],
            )

        return (
            results,
            totals,
        )

    for path, lines, words, bytes_ in results:
        print(
            "{:>6} {:>6} {:>6} {}".format(
                lines,
                words,
                bytes_,
                path,
            )
        )

    if len(paths) > 1:
        print(
            "{:>6} {:>6} {:>6} total".format(
                total_lines,
                total_words,
                total_bytes,
            )
        )

    return None
