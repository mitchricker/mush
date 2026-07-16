__doc__ = """
NAME
    cp - copy files

SYNOPSIS
    cp(src, dst, collect=False)

DESCRIPTION
    Copies a file using streamed I/O.

    Returns:
        collect=True:
            destination path

        collect=False:
            None on success
            False on failure

EXAMPLES
    cp(
        "a.txt",
        "b.txt",
    )

    cp(
        "a.txt",
        "b.txt",
        collect=True,
    )
"""

import mush

fsio = mush._load_internal("_fsio")


def main(
    src,
    dst,
    collect=False,
):
    if not src or not dst:
        print(
            "cp: missing file operand"
        )
        return False

    f = None

    try:
        f = fsio["open"](
            dst,
            "wb",
        )

        for chunk in fsio["read_chunks"](src):
            f.write(chunk)

        if collect:
            return dst

        print(
            "copied: {} -> {}".format(
                src,
                dst,
            )
        )

        return None

    except Exception as e:
        print(
            "cp: {}".format(e)
        )

        return False

    finally:
        if f:
            try:
                f.close()
            except Exception:
                pass
