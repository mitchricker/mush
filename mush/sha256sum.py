__doc__ = """
NAME
    sha256sum - calculate SHA-256 checksums

SYNOPSIS
    sha256sum(file1, [file2 ...], collect=False)

DESCRIPTION
    Calculates SHA-256 hashes of files.

    Returns:
        collect=True:
            list of:
                (
                    digest,
                    filename,
                )

        collect=False:
            None on success

        False on error

EXAMPLES
    sha256sum("boot.py")

    sha256sum(
        "a.txt",
        "b.txt",
    )

    sha256sum(
        "boot.py",
        collect=True,
    )
"""

import hashlib

import mush

fsio = mush._load_internal("_fsio")


def _hex(data):
    out = ""

    for b in data:
        out += "{:02x}".format(b)

    return out


def _sha256(path):
    h = hashlib.sha256()

    for chunk in fsio["read_chunks"](path):
        h.update(chunk)

    return _hex(
        h.digest()
    )


def main(*paths, collect=False):
    if not paths:
        print(
            "sha256sum: missing file"
        )
        return False

    results = []

    for path in paths:
        try:
            digest = _sha256(path)

        except Exception as e:
            print(
                "sha256sum: {}: {}".format(
                    path,
                    e,
                )
            )

            return False

        results.append(
            (
                digest,
                path,
            )
        )

        if not collect:
            print(
                "{}  {}".format(
                    digest,
                    path,
                )
            )

    if collect:
        return results

    return None
