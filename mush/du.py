__doc__ = """
NAME
    du - estimate file and directory space usage

SYNOPSIS
    du([path ...], human=False, summary=False, collect=False)

DESCRIPTION
    Displays disk usage for files and directories.

    Sizes are shown in bytes by default. Use human=True for
    human-readable sizes.

    Returns:
        collect=False:
            None on success

        collect=True:
            list of tuples:
            (
                path,
                bytes
            )

        False on failure

EXAMPLES
    du("/")

    du(
        "/logs",
        human=True,
    )

    du(
        "/config",
        summary=True,
    )

    du(
        "/tmp",
        collect=True,
    )
"""

import os
import mush

sys = mush._load_internal("_sys")


def _is_dir(path):
    try:
        return bool(
            os.stat(path)[0] & 0x4000
        )

    except Exception:
        return False


def _join(a, b):
    if a.endswith("/"):
        return a + b

    return a + "/" + b


def _size(path):
    try:
        st = os.stat(path)

    except Exception as e:
        raise OSError(
            "{}: {}".format(
                path,
                e,
            )
        )

    if not _is_dir(path):
        return st[6]

    total = 0

    for name in os.listdir(path):
        total += _size(
            _join(
                path,
                name,
            )
        )

    return total


def _format(size, human):
    if human:
        return sys["format_size"](
            size
        )

    return str(size)


def _emit(path, size, human):
    print(
        "{}\t{}".format(
            _format(
                size,
                human,
            ),
            path,
        )
    )


def _walk(
    path,
    human=False,
    summary=False,
):
    size = _size(path)

    if summary:
        _emit(
            path,
            size,
            human,
        )

        return

    if _is_dir(path):
        for name in os.listdir(path):
            child = _join(
                path,
                name,
            )

            if _is_dir(child):
                _walk(
                    child,
                    human,
                    False,
                )

    _emit(
        path,
        size,
        human,
    )


def main(
    *paths,
    human=False,
    summary=False,
    collect=False,
):
    if not paths:
        paths = (
            ".",
        )

    if collect:
        results = []

        try:
            for path in paths:
                results.append(
                    (
                        path,
                        _size(path),
                    )
                )

        except Exception as e:
            print(
                "du: {}".format(e)
            )

            return False

        return results

    try:
        for path in paths:
            _walk(
                path,
                human,
                summary,
            )

    except Exception as e:
        print(
            "du: {}".format(e)
        )

        return False

    return None
