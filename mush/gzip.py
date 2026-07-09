__doc__ = """
NAME
    gzip - compress files using gzip format

SYNOPSIS
    gzip(file)
    gzip(file, out)

DESCRIPTION
    Stream-based gzip compressor using MicroPython deflate.

    Compression support depends on firmware capabilities.

EXAMPLES
    gzip("test.txt")

    gzip("test.txt", "test.txt.gz")
"""
import deflate
def main(path, out=None):
    if not path:
        print("gzip: missing file")
        return
    if not hasattr(deflate, "compress"):
        raise OSError(
            "gzip compression not supported by this firmware"
        )
    if out is None:
        out = path + ".gz"
    src = open(path, "rb")
    try:
        dst = open(out, "wb")
        try:
            data = src.read()
            compressed = deflate.compress(
                data,
                deflate.GZIP,
            )
            dst.write(compressed)
        finally:
            dst.close()
    finally:
        src.close()
    return out
