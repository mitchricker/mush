__doc__ = """
NAME
    cmp - compare two files byte by byte

SYNOPSIS
    cmp(file1, file2)

DESCRIPTION
    Compares two files and reports the first difference.

EXAMPLES
    cmp(firmware1.bin, firmware2.bin)
"""
import mush
fsio = mush._load_internal("_fsio")
_CHUNK = 256
def main(file1, file2):
    if not file1 or not file2:
        print("cmp: missing file")
        return
    offset = 0
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
                b_buf = ""
        if not a_buf and not b_buf:
            return 0
        if not a_buf:
            print(
                "cmp: EOF on {} after {} bytes".format(
                    file1,
                    offset,
                )
            )
            return 1
        if not b_buf:
            print(
                "cmp: EOF on {} after {} bytes".format(
                    file2,
                    offset,
                )
            )
            return 1
        length = min(len(a_buf), len(b_buf))
        for i in range(length):
            if a_buf[i] != b_buf[i]:
                print(
                    "{} {} differ: byte {}, {:02x} != {:02x}".format(
                        file1,
                        file2,
                        offset,
                        a_buf[i],
                        b_buf[i],
                    )
                )
                return 1
            offset += 1
        a_buf = a_buf[length:]
        b_buf = b_buf[length:]
