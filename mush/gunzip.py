__doc__ = """
NAME
    gunzip - decompress gzip files

SYNOPSIS
    gunzip(file)
    gunzip(file, out)

DESCRIPTION
    Stream-based gzip decompressor using MicroPython deflate.

EXAMPLES
    gunzip("test.txt.gz")
"""
import deflate
def main(path, out=None):
    if not path:
        print("gunzip: missing file")
        return
    if out is None:
        if path.endswith(".gz"):
            out = path[:-3]
        else:
            out = path + ".out"
    src = open(path, "rb")
    try:
        dst = open(out, "wb")
        try:
            stream = deflate.DeflateIO(
                src,
                deflate.GZIP,
            )
            try:
                while True:
                    data = stream.read(256)
                    if not data:
                        break
                    dst.write(data)
            finally:
                stream.close()
        finally:
            dst.close()
    finally:
        src.close()
    return out
