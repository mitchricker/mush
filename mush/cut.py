__doc__ = """
NAME
    cut - extract portions of lines

SYNOPSIS
    cut(path, fields=None, delimiter="\\t",
        byte_ranges=None, out=None, collect=False)

DESCRIPTION
    Extracts fields or byte ranges from text.

    fields:
        Comma-separated 1-based field numbers.
        Example:
            "1,3,5"

    byte_ranges:
        Comma-separated 1-based byte positions or ranges.
        Example:
            "1-5,10"

    Returns:
        collect=True:
            list of extracted lines

        collect=False:
            True on success

        False on error

EXAMPLES
    cut("passwd", fields="1,3", delimiter=":")

    cut("file.txt", byte_ranges="1-10")

    cut("data.txt", fields="2", collect=True)
"""

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

            result.append(
                (
                    start,
                    end,
                )
            )

        else:
            n = int(part)

            result.append(
                (
                    n,
                    n,
                )
            )

    return result


def _select_bytes(data, ranges):
    out = bytearray()

    for start, end in ranges:
        start -= 1

        if end is None:
            out.extend(data[start:])

        else:
            out.extend(
                data[start:end]
            )

    return bytes(out)


def _select_fields(line, fields, delimiter):
    parts = line.split(delimiter)
    selected = []

    for start, end in fields:
        if end is None:
            end = len(parts)

        for index in range(
            start - 1,
            min(end, len(parts)),
        ):
            selected.append(
                parts[index]
            )

    return delimiter.join(selected)


def main(
    path,
    fields=None,
    delimiter="\t",
    byte_ranges=None,
    out=None,
    collect=False,
):
    if not path:
        print("cut: missing file")
        return False

    if fields is None and byte_ranges is None:
        print(
            "cut: specify fields= or byte_ranges="
        )
        return False

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

    except Exception as e:
        print(
            "cut: invalid range: {}".format(e)
        )
        return False

    if collect:
        result = []

        def emit(value):
            result.append(value)

        close = None

    else:
        write, close, get_result = fsio["output"](
            out=out,
        )

        def emit(value):
            write(value)
            write("\n")

    try:
        for line, terminated in fsio["iter_lines"](path):

            if byte_ranges_parsed is not None:
                value = fsio["decode"](
                    _select_bytes(
                        line,
                        byte_ranges_parsed,
                    )
                )

            else:
                value = _select_fields(
                    fsio["decode"](line),
                    field_ranges,
                    delimiter,
                )

            emit(value)

    except OSError as e:
        print(
            "cut: {}: {}".format(
                path,
                e,
            )
        )
        return False

    finally:
        if close:
            close()

    if collect:
        return result

    return get_result()
