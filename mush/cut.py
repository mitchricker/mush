__doc__ = """
NAME
    cut - extract portions of lines

SYNOPSIS
    cut(path, fields=None, delimiter="\\t", byte_ranges=None, out=None)

DESCRIPTION
    Extract fields or byte ranges from text.

    fields:
        Comma-separated 1-based field numbers.
        Example: "1,3,5"

    byte_ranges:
        Comma-separated 1-based byte positions or ranges.
        Example: "1-5,10"

EXAMPLES
    cut("passwd", fields="1,3", delimiter=":")
    cut("file.txt", byte_ranges="1-10")
"""
import sys
import mush
fsio = mush._load_internal("_fsio")
def _parse_list(spec):
    result = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            start = int(a) if a else 1
            end = int(b) if b else None
            result.append((start, end))
        else:
            n = int(part)
            result.append((n, n))
    return result
def _select_bytes(data, ranges):
    out = bytearray()
    for start, end in ranges:
        start -= 1
        if end is None:
            out.extend(data[start:])
        else:
            out.extend(data[start:end])
    return out
def _select_fields(line, fields, delimiter):
    parts = line.split(delimiter)
    selected = []
    for start, end in fields:
        if end is None:
            end = len(parts)
        for index in range(start - 1, min(end, len(parts))):
            selected.append(parts[index])
    return delimiter.join(selected)
def _decode(data):
    try:
        return data.decode("utf-8")
    except Exception:
        return data.decode()
def _write(out, text, terminated):
    if out:
        out.write(text)
        if terminated:
            out.write("\n")
    else:
        sys.stdout.write(text)
        if terminated:
            sys.stdout.write("\n")
def main(path, fields=None, delimiter="\t", byte_ranges=None, out=None):
    if not path:
        print("cut: missing file")
        return
    if fields is None and byte_ranges is None:
        print("cut: specify fields= or byte_ranges=")
        return
    close_out = False
    if isinstance(out, str):
        out = open(out, "w")
        close_out = True
    try:
        field_ranges = (
            _parse_list(fields)
            if fields is not None
            else None
        )
        byte_ranges_parsed = (
            _parse_list(byte_ranges)
            if byte_ranges is not None
            else None
        )
        for line, terminated in fsio["iter_lines"](path):
            if byte_ranges_parsed is not None:
                result = _decode(
                    _select_bytes(
                        line,
                        byte_ranges_parsed,
                    )
                )
            else:
                result = _select_fields(
                    _decode(line),
                    field_ranges,
                    delimiter,
                )
            _write(
                out,
                result,
                terminated,
            )
    finally:
        if close_out:
            out.close()
