__doc__ = """
NAME
    xxd - deterministic binary hex dump and restore tool

SYNOPSIS
    xxd(path, machine=True, out=None, width=16,
        reverse=False, collect=False)

DESCRIPTION
    Hex dump / restore utility for MicroPython.

    Modes:
      machine=True
          lossless hex dump (default)

      machine=False
          human-readable dump

      reverse=True
          restore from machine dump (requires out file)

    Returns:
        collect=False:
            None on success
            False on failure

        collect=True:
            Generated dump text

            reverse=True:
                Number of bytes restored

EXAMPLES
    xxd("file.bin")

    xxd(
        "file.bin",
        machine=False,
    )

    xxd(
        "dump.hex",
        reverse=True,
        out="file.bin",
    )

    xxd(
        "file.bin",
        collect=True,
    )
"""

import mush

fsio = mush._load_internal("_fsio")

_CHUNK = 256


def _dump_machine(path, width, emit):
    offset = 0
    buf = []

    def flush():
        nonlocal offset, buf

        if not buf:
            return

        hex_bytes = "".join(
            "{:02x}".format(b)
            for b in buf
        )

        emit(
            "{:08x} {}".format(
                offset,
                hex_bytes,
            )
        )

        offset += len(buf)
        buf = []

    for chunk in fsio["read_chunks"](
        path,
        _CHUNK,
    ):
        for b in chunk:
            buf.append(b)

            if len(buf) == width:
                flush()

    flush()


def _dump_human(path, width, emit):
    offset = 0
    buf = []

    def flush():
        nonlocal offset, buf

        if not buf:
            return

        hex_part = []
        ascii_part = []

        for b in buf:
            hex_part.append(
                "{:02x}".format(b)
            )

            ascii_part.append(
                chr(b)
                if 32 <= b <= 126
                else "."
            )

        emit(
            "{:08x}: {:<48} |{}|".format(
                offset,
                " ".join(hex_part),
                "".join(ascii_part),
            )
        )

        offset += len(buf)
        buf = []

    for chunk in fsio["read_chunks"](
        path,
        _CHUNK,
    ):
        for b in chunk:
            buf.append(b)

            if len(buf) == width:
                flush()

    flush()


def _restore_machine(path, out):
    count = 0

    for line in fsio["iter_lines"](path):
        data, terminated = line

        try:
            text = data.decode().strip()

        except Exception:
            continue

        if not text:
            continue

        parts = text.split()

        if len(parts) != 2:
            continue

        hexdata = parts[1]

        for i in range(
            0,
            len(hexdata),
            2,
        ):
            out.write(
                bytes(
                    [
                        int(
                            hexdata[i:i + 2],
                            16,
                        )
                    ]
                )
            )

            count += 1

    return count


def main(
    path,
    machine=True,
    out=None,
    width=16,
    reverse=False,
    collect=False,
):
    if not path:
        print(
            "xxd: missing file"
        )
        return False

    output = []

    close_out = False
    file_out = None

    try:
        if reverse:
            if out is None:
                print(
                    "xxd: reverse requires out=<file path>"
                )
                return False

            file_out = open(
                out,
                "wb",
            )
            close_out = True

            count = _restore_machine(
                path,
                file_out,
            )

            return count if collect else None

        def emit(line):
            if collect:
                output.append(line)

            else:
                if out:
                    out.write(
                        line + "\n"
                    )
                else:
                    print(line)

        if isinstance(out, str):
            file_out = open(
                out,
                "w",
            )
            close_out = True

            def emit(line):
                if collect:
                    output.append(line)

                else:
                    file_out.write(
                        line + "\n"
                    )

        if machine:
            _dump_machine(
                path,
                width,
                emit,
            )

        else:
            _dump_human(
                path,
                width,
                emit,
            )

        if collect:
            return "\n".join(output)

        return None

    except Exception as e:
        print(
            "xxd:",
            e,
        )

        return False

    finally:
        if close_out:
            try:
                file_out.close()

            except Exception:
                pass
