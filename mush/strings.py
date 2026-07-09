__doc__ = """
NAME
    strings - extract printable strings from binary files

SYNOPSIS
    strings(path, minlen=4, out=None)

DESCRIPTION
    Scans a binary file and prints sequences of printable ASCII
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
def _emit(buf, out):
    if not buf:
        return
    s = bytes(buf).decode()
    if out:
        out.write(s + "\n")
    else:
        print(s)
def main(path, minlen=4, out=None):
    if not path:
        print("strings: missing file")
        return
    close_out = False
    if isinstance(out, str):
        out = open(out, "w")
        close_out = True
    try:
        buf = bytearray()
        for chunk in fsio["read_chunks"](path, _CHUNK):
            for b in chunk:
                if b == 9 or 32 <= b <= 126:
                    buf.append(b)
                else:
                    if len(buf) >= minlen:
                        _emit(buf, out)
                    buf = bytearray()
        if len(buf) >= minlen:
            _emit(buf, out)
    finally:
        if close_out:
            out.close()
