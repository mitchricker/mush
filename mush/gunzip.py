__doc__ = """
NAME
    gunzip - decompress gzip files

SYNOPSIS
    gunzip(path, out=None)

DESCRIPTION
    Decompresses gzip files.

    If OUT is omitted and PATH ends in .gz,
    the suffix is removed.

EXAMPLES
    gunzip("firmware.bin.gz")
"""
import mush
import deflate
fsio = mush._load_internal("_fsio")
_CHUNK = 256
def main(path, out=None):
    if not path:
        print("gunzip: missing file")
        return
    if out is None:
        if path.endswith(".gz"):
            out = path[:-3]
        else:
            out = path + ".out"
    write, close = fsio["write_stream"](out)
    f = open(path, "rb")
    try:
        dec = deflate.DeflateIO(
            f,
            deflate.DECOMPRESS,
            deflate.FORMAT_GZIP,
        )
        while True:
            data = dec.read(_CHUNK)
            if not data:
                break
            write(data)
        dec.close()
    finally:
        f.close()
        close()
