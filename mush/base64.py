__doc__ = """
NAME
    base64 - encode/decode files using Base64

SYNOPSIS
    base64 encode file
    base64 decode file

DESCRIPTION
    Stream-based Base64 encoder/decoder.

    Designed for MicroPython constraints:
    - no full file buffering
    - chunked processing
    - minimal RAM usage

EXAMPLES
    base64 encode image.bin

    base64 decode data.b64
"""
import sys
import mush._fsio as fsio
_B64 = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
def _encode_block(block):
    out = []
    # pad to 3 bytes
    while len(block) < 3:
        block += b"\x00"
    n = (block[0] << 16) + (block[1] << 8) + block[2]
    out.append(_B64[(n >> 18) & 63])
    out.append(_B64[(n >> 12) & 63])
    out.append(_B64[(n >> 6) & 63])
    out.append(_B64[n & 63])
    return out
def _encode_stream(path):
    buf = b""
    for chunk in fsio.read_chunks(path):
        buf += chunk
        while len(buf) >= 3:
            block = buf[:3]
            buf = buf[3:]
            for b in _encode_block(block):
                sys.stdout.buffer.write(bytes([b]))
    # final padding
    if buf:
        pad_len = 3 - len(buf)
        block = buf + b"\x00" * pad_len
        encoded = _encode_block(block)
        for i in range(pad_len):
            encoded[-(i + 1)] = ord("=")
        sys.stdout.buffer.write(bytes(encoded))
def _decode_block(block):
    vals = []
    for c in block:
        if c == ord("="):
            vals.append(0)
        else:
            vals.append(_B64.index(c))
    n = (vals[0] << 18) + (vals[1] << 12) + (vals[2] << 6) + vals[3]
    return bytes([
        (n >> 16) & 255,
        (n >> 8) & 255,
        n & 255,
    ])
def _decode_stream(path):
    buf = b""
    for chunk in fsio.read_chunks(path):
        buf += chunk
        # strip whitespace
        buf = b"".join(buf.split())
        while len(buf) >= 4:
            block = buf[:4]
            buf = buf[4:]
            decoded = _decode_block(block)
            sys.stdout.buffer.write(decoded)
def main(mode, path):
    if mode == "encode":
        _encode_stream(path)
    elif mode == "decode":
        _decode_stream(path)
    else:
        print("usage: base64 encode|decode file")
