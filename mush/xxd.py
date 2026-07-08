__doc__ = """
NAME
    xxd - deterministic binary hex dump and restore tool

SYNOPSIS
    xxd(path, machine=True, out=None, width=16, reverse=False)

DESCRIPTION
    Hex dump / restore utility for MicroPython.

    Modes:
      machine=True   lossless hex dump (default)
      machine=False  human-readable dump
      reverse=True   restore from machine dump (requires out file)

EXAMPLES
    xxd("file.bin")
    xxd("file.bin", machine=False)
    xxd("dump.hex", reverse=True, out="file.bin")
"""

from mush._fsio import read_chunks

_CHUNK = 256

def _dump_machine(path, width, out):
    offset = 0
    buf = []

    def emit(data, off):
        hex_bytes = "".join("{:02x}".format(b) for b in data)
        line = "{:08x} {}".format(off, hex_bytes)

        if out:
            out.write(line + "\n")
        else:
            print(line)

    for chunk in read_chunks(path, _CHUNK):
        for b in chunk:
            buf.append(b)
            if len(buf) == width:
                emit(buf, offset)
                offset += width
                buf = []

    if buf:
        emit(buf, offset)

def _dump_human(path, width, out):
    offset = 0
    buf = []

    def emit():
        nonlocal offset, buf

        hex_part = []
        ascii_part = []

        for b in buf:
            hex_part.append("{:02x}".format(b))
            ascii_part.append(chr(b) if 32 <= b <= 126 else ".")

        line = "{:08x}: {:<48} |{}|".format(
            offset,
            " ".join(hex_part),
            "".join(ascii_part),
        )

        if out:
            out.write(line + "\n")
        else:
            print(line)

        offset += len(buf)
        buf = []

    for chunk in read_chunks(path, _CHUNK):
        for b in chunk:
            buf.append(b)
            if len(buf) == width:
                emit()

    if buf:
        emit()

def _restore_machine(path, out_file):
    f = open(out_file, "wb")
    try:
        for line in read_chunks(path):
            try:
                s = line.decode().strip()
            except:
                continue

            if not s:
                continue

            parts = s.split()
            if len(parts) != 2:
                continue

            hexdata = parts[1]

            i = 0
            while i < len(hexdata):
                f.write(bytes([int(hexdata[i:i+2], 16)]))
                i += 2
    finally:
        f.close()

def main(path, machine=True, out=None, width=16, reverse=False):

    if not path:
        print("xxd: missing file")
        return

    # normalize output file string -> file handle
    close_out = False
    if isinstance(out, str):
        out = open(out, "w")
        close_out = True

    try:
        # reverse mode overrides everything else
        if reverse:
            if not isinstance(out, str) and out is None:
                print("xxd: reverse requires out=<file path>")
                return
            return _restore_machine(path, out)

        if machine:
            return _dump_machine(path, width, out)
        else:
            return _dump_human(path, width, out)

    finally:
        if close_out:
            out.close()
