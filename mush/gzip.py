__doc__ = """
NAME
    gzip - compress files using gzip format

SYNOPSIS
    gzip(file, out=None, collect=False)

DESCRIPTION
    Stream-based gzip compressor using MicroPython deflate.

    Compression support depends on firmware capabilities.

    Returns:
        collect=False:
            None on success.

        collect=True:
            Output path.

        False on failure.

EXAMPLES
    gzip(
        "test.txt"
    )

    gzip(
        "test.txt",
        out="test.txt.gz",
    )

    gzip(
        "test.txt",
        collect=True,
    )
"""

import deflate
import mush

fsio = mush._load_internal("_fsio")


def main(
    path,
    out=None,
    collect=False,
):
    if not path:
        print(
            "gzip: missing file"
        )

        return False

    try:
        if not hasattr(
            deflate,
            "DeflateIO",
        ):
            raise OSError(
                "gzip streaming not supported by this firmware"
            )

        if out is None:
            out = path + ".gz"

        dst = open(
            out,
            "wb",
        )

        try:
            gz = deflate.DeflateIO(
                dst,
                deflate.GZIP,
            )

            try:
                for chunk in fsio["read_chunks"](path):
                    gz.write(chunk)

            finally:
                gz.close()

        finally:
            dst.close()

    except Exception as e:
        print(
            "gzip: {}".format(e)
        )

        return False

    if collect:
        return out

    print(
        "compressed: {} -> {}".format(
            path,
            out,
        )
    )

    return None
