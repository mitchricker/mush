"""
Internal filesystem I/O helper.

Provides:
    read_chunks()
    iter_lines()
    iter_lines_reverse()
    decode()
    output()

Functions:

    read_chunks(path, chunk=256)

        Yield file contents in chunks.


    iter_lines(path)

        Iterate file lines.

        Returns:
            (
                line_bytes,
                newline_present
            )


    iter_lines_reverse(path)

        Iterate file lines in reverse order.


    decode(data)

        Decode byte data into text.


    output(out=None, collect=False)

        Create an output writer.

        Returns:
            (
                write_function,
                close_function,
                result_function
            )

        collect=True:
            result() returns collected output.

        collect=False:
            result() returns True.
"""
import sys

_CHUNK = 256


def read_chunks(path, chunk=_CHUNK):
    f = open(path, "rb")
    try:
        while True:
            b = f.read(chunk)
            if not b:
                break
            yield b
    finally:
        f.close()


def output(out=None, collect=False):
    if collect:
        parts = []
        kind = None

        def write(data):
            nonlocal kind

            if kind is None:
                kind = bytes if isinstance(data, bytes) else str

            parts.append(data)

        def close():
            pass

        def result():
            if kind is bytes:
                return b"".join(parts)

            if kind is str:
                return "".join(parts)

            return None

        return write, close, result

    if isinstance(out, str):
        f = open(out, "wb")

        def write(data):
            if isinstance(data, str):
                data = data.encode()
            f.write(data)

        def close():
            try:
                f.flush()
            finally:
                f.close()

        def result():
            return True

        return write, close, result

    def write(data):
        if isinstance(data, bytes):
            try:
                sys.stdout.buffer.write(data)
            except AttributeError:
                sys.stdout.write(data.decode("utf-8", "ignore"))
        else:
            sys.stdout.write(data)

    def close():
        try:
            sys.stdout.flush()
        except Exception:
            pass

    def result():
        return True

    return write, close, result


def decode(data):
    if isinstance(data, str):
        return data

    try:
        return data.decode("utf-8", "ignore")
    except Exception:
        return str(data)


def copy(src, dst, chunk=_CHUNK):
    out = open(dst, "wb")
    try:
        for b in read_chunks(src, chunk):
            out.write(b)
    finally:
        out.close()


def atomic_write(dst, write_fn, replace=True):
    import os

    tmp = dst + ".tmp"

    try:
        f = open(tmp, "wb")
        try:
            write_fn(f)
            try:
                f.flush()
            except Exception:
                pass
        finally:
            f.close()

        if replace:
            try:
                os.remove(dst)
            except Exception:
                pass

        os.rename(tmp, dst)

    except Exception:
        try:
            os.remove(tmp)
        except Exception:
            pass
        raise


def iter_lines(path):
    buf = b""

    for chunk in read_chunks(path):
        start = 0

        for i in range(len(chunk)):
            if chunk[i] == 10:
                yield buf + chunk[start:i], True
                buf = b""
                start = i + 1

        if start < len(chunk):
            buf += chunk[start:]

    if buf:
        yield buf, False


def _reverse(data):
    out = bytearray(len(data))

    for i in range(len(data)):
        out[i] = data[len(data) - i - 1]

    return bytes(out)


def iter_lines_reverse(path, chunk=_CHUNK):
    f = open(path, "rb")

    try:
        f.seek(0, 2)
        pos = f.tell()

        buf = bytearray()

        while pos > 0:
            size = min(chunk, pos)
            pos -= size

            f.seek(pos)
            data = f.read(size)

            for i in range(len(data) - 1, -1, -1):
                if data[i] == 10:
                    if buf:
                        yield _reverse(buf)
                        buf = bytearray()
                else:
                    buf.append(data[i])

        if buf:
            yield _reverse(buf)

    finally:
        f.close()
