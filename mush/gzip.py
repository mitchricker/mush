__doc__ = """
NAME
    gzip - compress files using gzip format

SYNOPSIS
    gzip(path, out=None)

DESCRIPTION
    Compresses PATH into gzip format.

    If OUT is omitted, writes PATH + ".gz".

EXAMPLES
    gzip("firmware.bin")
    gzip("log.txt", out="log.gz")
"""
import mush
import deflate
fsio = mush._load_internal("_fsio")
_CHUNK = 256
def main(path, out=None):
    if not path:
        print("gzip: missing file")
        return
    if out is None:
        out = path + ".gz"
    write, close = fsio["write_stream"](out)
    try:
        # gzip wrapper
        comp = deflate.DeflateIO(
            write,
            deflate.COMPRESS,
            deflate.FORMAT_GZIP,
        )
        for chunk in fsio["read_chunks"](path, _CHUNK):
            comp.write(chunk)
        comp.close()
    finally:
        close()
