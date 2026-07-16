__doc__ = """
NAME
    cut - extract portions of lines

SYNOPSIS
    cut(path, fields=None, delimiter="\\t", byte_ranges=None,
        out=None, collect=False)

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
            None on success
            False on error

EXAMPLES
    cut(
        "passwd",
        fields="1,3",
        delimiter=":",
    )

    cut(
        "file.txt",
        byte_ranges="1-10",
    )

    cut(
        "data.txt",
        fields="2",
        collect=True,
    )
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
            start, end = part.split("-", 1)

            result.append(
                (
                    int(start) if start else 1,
                    int(end) if end else None,
                )
            )

        else:
            value = int(part)

            result.append(
                (
                    value,
                    value,
                )
            )

    return result


def _select_bytes(data, ranges):
    result = bytearray()

    for start, end in ranges:
        start -= 1

        if end is None:
            result.extend(
                data[start:]
            )

        else:
            result.extend(
                data[start:end]
            )

    return bytes(result)


def _select_fields(line, fields, delimiter):
    parts = line.split(delimiter)
    result = []

    for start, end in fields:
        if end is None:
            end = len(parts)

        result.extend(
            parts[
                start - 1:min(
                    end,
                    len(parts),
                )
            ]
        )

    return delimiter.join(result)


def main(
    path,
    fields=None,
    delimiter="\t",
    byte_ranges=None,
    out=None,
    collect=False,
):
    if not path:
        print(
            "cut: missing file"
        )
        return False

    if (
        fields is None
        and byte_ranges is None
    ):
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

    values = []

    if not collect:
        write, close, _ = fsio["output"](
            out=out,
        )

    else:
        write = None
        close = None

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

            if collect:
                values.append(value)

            else:
                write(value)
                write("\n")

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
        return values

    return None