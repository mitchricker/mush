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
def write_stream(path):
    f = open(path, "wb")
    def write(data):
        f.write(data)
    def close():
        try:
            f.flush()
        finally:
            f.close()
    return write, close
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
