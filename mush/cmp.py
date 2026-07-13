__doc__ = """
NAME
    cmp - compare two files byte by byte

SYNOPSIS
    cmp(file1, file2, collect=False)

DESCRIPTION
    Compares two files and reports the first difference.

    Returns:
        True  - files are identical
        False - files differ
        None  - comparison error

EXAMPLES
    cmp("firmware1.bin", "firmware2.bin")

    cmp("a.bin", "b.bin", collect=True)
"""

import mush

fsio = mush._load_internal("_fsio")

_CHUNK = 256


def main(file1, file2, collect=False):
    if not file1 or not file2:
        msg = "cmp: missing file"

        if collect:
            return msg

        print(msg)
        return None

    offset = 0

    try:
        a_iter = fsio["read_chunks"](file1, _CHUNK)
        b_iter = fsio["read_chunks"](file2, _CHUNK)

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
                    b_buf = b""

            if not a_buf and not b_buf:
                return True

            if not a_buf:
                msg = (
                    "cmp: EOF on {} after {} bytes"
                    .format(file1, offset)
                )

                if collect:
                    return msg

                print(msg)
                return False

            if not b_buf:
                msg = (
                    "cmp: EOF on {} after {} bytes"
                    .format(file2, offset)
                )

                if collect:
                    return msg

                print(msg)
                return False

            length = min(
                len(a_buf),
                len(b_buf),
            )

            for i in range(length):
                if a_buf[i] != b_buf[i]:
                    msg = (
                        "{} {} differ: byte {}, "
                        "{:02x} != {:02x}"
                    ).format(
                        file1,
                        file2,
                        offset,
                        a_buf[i],
                        b_buf[i],
                    )

                    if collect:
                        return msg

                    print(msg)
                    return False

                offset += 1

            a_buf = a_buf[length:]
            b_buf = b_buf[length:]

    except OSError as e:
        msg = "cmp: {}".format(e)

        if collect:
            return msg

        print(msg)
        return None
