__doc__ = """
NAME
    strings - extract printable strings from binary files

SYNOPSIS
    strings(path, minlen=4, out=None, collect=False)

DESCRIPTION
    Scans a binary file and extracts sequences of printable ASCII
    characters.

    Printable characters are in the range 0x20-0x7e, along with
    tab ('\\t').

    Strings shorter than minlen are ignored.

EXAMPLES
    strings("firmware.bin")
    strings("image.raw", minlen=8)
    strings("flash.bin", out="strings.txt")
"""

import mush

fsio = mush._load_internal("_fsio")

_CHUNK = 256


def _emit(buf, write):
    if not buf:
        return

    write(bytes(buf).decode())
    write("\n")


def main(path, minlen=4, out=None, collect=False):
    if not path:
        print("strings: missing file")
        return False

    write, close, result = fsio["output"](
        out=out,
        collect=collect,
    )

    try:
        buf = bytearray()

        for chunk in fsio["read_chunks"](path, _CHUNK):
            for b in chunk:
                if b == 9 or 32 <= b <= 126:
                    buf.append(b)
                else:
                    if len(buf) >= minlen:
                        _emit(buf, write)
                    buf = bytearray()

        if len(buf) >= minlen:
            _emit(buf, write)

    finally:
        close()

    return result()
