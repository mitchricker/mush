__doc__ = """
NAME
    cmp - compare two files byte by byte

SYNOPSIS
    cmp(file1, file2, collect=False)

DESCRIPTION
    Compares two files and reports the first difference.

    Returns:

        collect=False:
            None on success
            False on failure

        collect=True:
            (
                identical,
                message,
            )

            identical:
                True  - files match
                False - files differ

            message:
                Difference or error text.

EXAMPLES
    cmp(
        "firmware1.bin",
        "firmware2.bin",
    )

    cmp(
        "a.bin",
        "b.bin",
        collect=True,
    )
"""

import mush

fsio = mush._load_internal("_fsio")

_CHUNK = 256


def _fail(message, collect):
    if collect:
        return (
            False,
            message,
        )

    print(message)
    return False


def _done(identical, message, collect):
    if collect:
        return (
            identical,
            message,
        )

    if message:
        print(message)
        return False

    return None


def main(file1, file2, collect=False):
    if not file1 or not file2:
        return _fail(
            "cmp: missing file",
            collect,
        )

    offset = 0

    try:
        a_iter = fsio["read_chunks"](
            file1,
            _CHUNK,
        )

        b_iter = fsio["read_chunks"](
            file2,
            _CHUNK,
        )

        a_buf = b""
        b_buf = b""

        while True:
            if not a_buf:
                try:
                    a_buf = next(a_iter)
                except StopIteration:
                    a_buf = b""

            if not b_buf:
                try:
                    b_buf = next(b_iter)
                except StopIteration:
                    b_buf = ""

            if not a_buf and not b_buf:
                return _done(
                    True,
                    None,
                    collect,
                )

            if not a_buf:
                return _done(
                    False,
                    "cmp: EOF on {} after {} bytes".format(
                        file1,
                        offset,
                    ),
                    collect,
                )

            if not b_buf:
                return _done(
                    False,
                    "cmp: EOF on {} after {} bytes".format(
                        file2,
                        offset,
                    ),
                    collect,
                )

            length = min(
                len(a_buf),
                len(b_buf),
            )

            for i in range(length):
                if a_buf[i] != b_buf[i]:
                    return _done(
                        False,
                        (
                            "{} {} differ: "
                            "byte {}, {:02x} != {:02x}"
                        ).format(
                            file1,
                            file2,
                            offset,
                            a_buf[i],
                            b_buf[i],
                        ),
                        collect,
                    )

                offset += 1

            a_buf = a_buf[length:]
            b_buf = b_buf[length:]

    except Exception as e:
        return _fail(
            "cmp: {}".format(e),
            collect,
        )
