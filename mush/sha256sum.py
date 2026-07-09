__doc__ = """
NAME
    sha256sum - calculate SHA-256 checksums

SYNOPSIS
    sha256sum(file1, [file2 ...])

DESCRIPTION
    Calculates SHA-256 hashes of files.

EXAMPLES
    sha256sum("boot.py")
    sha256sum("a.txt", "b.txt")
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
    return _hex(h.digest())
def main(*paths):
    if not paths:
        print("sha256sum: missing file")
        return
    for path in paths:
        try:
            print(
                "{}  {}".format(
                    _sha256(path),
                    path,
                )
            )
        except Exception as e:
            print(
                "sha256sum: {}: {}".format(
                    path,
                    e,
                )
            )
