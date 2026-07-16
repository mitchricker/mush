__doc__ = """
NAME
    base64 - encode/decode files using Base64

SYNOPSIS
    base64(file, decode=False, out=None, collect=False)

DESCRIPTION
    Stream-based Base64 encoder/decoder.

OPTIONS
    decode:
        Decode Base64 input instead of encoding.

    out:
        Write output to a file instead of stdout.

    collect:
        Return generated output instead of writing.

RETURNS
    collect=False:
        None on success
        False on failure

    collect=True:
        Generated Base64 data.

EXAMPLES
    base64(
        "image.bin"
    )

    base64(
        "data.b64",
        decode=True,
    )

    base64(
        "image.bin",
        collect=True,
    )
"""

import mush

fsio = mush._load_internal("_fsio")


_B64 = (
    b"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    b"abcdefghijklmnopqrstuvwxyz"
    b"0123456789+/"
)


def _encode_block(block):
    while len(block) < 3:
        block += b"\x00"

    n = (
        (block[0] << 16)
        |
        (block[1] << 8)
        |
        block[2]
    )

    return bytes((
        _B64[(n >> 18) & 63],
        _B64[(n >> 12) & 63],
        _B64[(n >> 6) & 63],
        _B64[n & 63],
    ))


def _decode_value(c):
    if c == ord("="):
        return 0

    value = _B64.find(
        bytes((c,))
    )

    if value < 0:
        raise ValueError(
            "invalid Base64 character"
        )

    return value


def _decode_block(block):
    vals = (
        _decode_value(block[0]),
        _decode_value(block[1]),
        _decode_value(block[2]),
        _decode_value(block[3]),
    )

    n = (
        (vals[0] << 18)
        |
        (vals[1] << 12)
        |
        (vals[2] << 6)
        |
        vals[3]
    )

    out = bytes((
        (n >> 16) & 255,
        (n >> 8) & 255,
        n & 255,
    ))

    if block[3] == ord("="):
        out = out[:-1]

    if block[2] == ord("="):
        out = out[:-1]

    return out


def _encode_stream(path, write):
    buf = b""

    for chunk in fsio["read_chunks"](path):

        buf += chunk

        while len(buf) >= 3:

            write(
                _encode_block(
                    buf[:3]
                ).decode("ascii")
            )

            buf = buf[3:]

    if buf:

        pad = 3 - len(buf)

        encoded = bytearray(
            _encode_block(
                buf + (b"\x00" * pad)
            )
        )

        for i in range(pad):
            encoded[-(i + 1)] = ord("=")

        write(
            bytes(encoded).decode(
                "ascii"
            )
        )

    write("\n")


def _decode_stream(path, write):
    buf = b""

    for chunk in fsio["read_chunks"](path):

        buf += b"".join(
            chunk.split()
        )

        while len(buf) >= 4:

            write(
                _decode_block(
                    buf[:4]
                )
            )

            buf = buf[4:]

    if buf:
        raise ValueError(
            "invalid Base64 length"
        )


def main(
    path,
    decode=False,
    out=None,
    collect=False,
):
    if not path:
        print(
            "base64: missing file"
        )
        return False

    write, close, result = fsio["output"](
        out=out,
        collect=collect,
    )

    try:
        if decode:
            _decode_stream(
                path,
                write,
            )

        else:
            _encode_stream(
                path,
                write,
            )

    except Exception as e:
        print(
            "base64: {}".format(
                e
            )
        )

        return False

    finally:
        close()

    return result()
