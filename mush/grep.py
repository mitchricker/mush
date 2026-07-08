__doc__ = """
NAME
    grep - search text for a pattern

SYNOPSIS
    grep(pattern, path, ...)
    grep(pattern, path, ..., ignore_case=True)

DESCRIPTION
    Searches files for lines matching a regular expression.

    Options:
        ignore_case - perform case-insensitive matching

EXAMPLES
    grep("wifi", "boot.py")
    grep("^import", "main.py")
    grep("error|fail", "log.txt")
    grep("warning", "log.txt", ignore_case=True)
"""

import re
import mush._fsio as fsio


def _grep_file(regex, path):
    try:
        for lineno, line in enumerate(fsio.iter_lines(path), 1):
            try:
                text = line.decode()
            except Exception:
                text = str(line)

            if regex.search(text):
                print("{}:{}:{}".format(path, lineno, text))

    except OSError as e:
        print("grep: {}: {}".format(path, e))
    except Exception as e:
        print("grep: {}: {}".format(path, e))


def main(pattern, *paths, ignore_case=False):
    if not paths:
        print("usage: grep(pattern, path, ...)")
        return

    flags = 0

    if ignore_case:
        flags |= re.IGNORECASE

    try:
        regex = re.compile(pattern, flags)
    except Exception as e:
        print("grep: invalid pattern: {}".format(e))
        return

    for path in paths:
        _grep_file(regex, path)
