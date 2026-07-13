__doc__ = """
NAME
    md5sum - calculate MD5 checksums

SYNOPSIS
    md5sum(file1, [file2 ...])

DESCRIPTION
    Calculates MD5 hashes of files.

    MD5 is intended for file integrity checking only.
    It is not suitable for cryptographic security.

EXAMPLES
    md5sum("boot.py")

    md5sum("a.txt", "b.txt")
"""

import hashlib

import mush

fsio = mush._load_internal("_fsio")


def _hex(data):
    out = ""

    for b in data:
        out += "{:02x}".format(b)

    return out


def _md5(path):
    h = hashlib.md5()

    for chunk in fsio["read_chunks"](path):
        h.update(chunk)

    return _hex(h.digest())


def main(*paths):
    if not paths:
        print("md5sum: missing file")
        return False

    results = []
    success = True

    for path in paths:
        try:
            digest = _md5(path)

            print(
                "{}  {}".format(
                    digest,
                    path,
                )
            )

            results.append(
                (digest, path)
            )

        except Exception as e:
            print(
                "md5sum: {}: {}".format(
                    path,
                    e,
                )
            )
            success = False

    if not success:
        return False

    if len(results) == 1:
        return results[0][0]

    return results
