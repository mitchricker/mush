__doc__ = """
NAME
    gunzip - decompress gzip files

SYNOPSIS
    gunzip(file, out=None, collect=False)

DESCRIPTION
    Stream-based gzip decompressor using MicroPython deflate.

    Returns:
        collect=False:
            None on success.

        collect=True:
            Output path.

        False on failure.

EXAMPLES
    gunzip(
        "test.txt.gz"
    )

    gunzip(
        "test.txt.gz",
        out="test.txt",
        collect=True,
    )
"""

import deflate


def main(
    path,
    out=None,
    collect=False,
):
    if not path:
        print(
            "gunzip: missing file"
        )

        return False

    try:
        if out is None:
            if path.endswith(".gz"):
                out = path[:-3]

            else:
                out = path + ".out"

        src = open(
            path,
            "rb",
        )

        try:
            dst = open(
                out,
                "wb",
            )

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

    except Exception as e:
        print(
            "gunzip: {}".format(e)
        )

        return False

    if collect:
        return out

    print(
        "decompressed: {} -> {}".format(
            path,
            out,
        )
    )

    return None
