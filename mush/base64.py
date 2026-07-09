__doc__ = """
NAME
    base64 - encode/decode files using Base64

SYNOPSIS
    base64(file)
    base64(file, decode=True)

DESCRIPTION
    Stream-based Base64 encoder/decoder.

EXAMPLES
    base64("image.bin")

    base64("data.b64", decode=True)
"""

import sys
import mush

fsio = mush._load_internal("_fsio")

_B64 = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


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


def _encode_stream(path):
    buf = b""

    for chunk in fsio["read_chunks"](path):
        buf += chunk

        while len(buf) >= 3:
            block = buf[:3]
            buf = buf[3:]

            sys.stdout.buffer.write(
                _encode_block(block)
            )

    if buf:
        pad = 3 - len(buf)

        encoded = bytearray(
            _encode_block(buf + b"\x00" * pad)
        )

        for i in range(pad):
            encoded[-(i + 1)] = ord("=")

        sys.stdout.buffer.write(bytes(encoded))
        
    sys.stdout.buffer.write(b"\n")


def _decode_value(c):
    if c == ord("="):
        return 0

    # MicroPython-safe lookup
    return _B64.find(bytes((c,)))


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


def _decode_stream(path):
    buf = b""

    for chunk in fsio["read_chunks"](path):
        buf += chunk

        # Remove whitespace from Base64 stream
        buf = b"".join(buf.split())

        while len(buf) >= 4:
            block = buf[:4]
            buf = buf[4:]

            sys.stdout.buffer.write(
                _decode_block(block)
            )

    if buf:
        raise ValueError("invalid Base64 length")

def main(path, decode=False):
    if decode:
        _decode_stream(path)
    else:
        _encode_stream(path)