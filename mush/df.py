__doc__ = """
NAME
    df - display filesystem usage

SYNOPSIS
    df(path="/", collect=False)

DESCRIPTION
    Displays filesystem size and usage.

    Returns:

        collect=False:
            None on success
            False on error

        collect=True:
            (
                path,
                total bytes,
                used bytes,
                usage percentage,
                free bytes
            )

            False on error

EXAMPLES
    df()

    df(
        "/system"
    )

    df(
        "/flash",
        collect=True,
    )
"""

import mush

sys = mush._load_internal("_sys")


def main(
    path="/",
    collect=False,
):
    try:
        (
            block,
            blocks,
            blocks_free,
            total,
            used,
            free,
        ) = sys["fs_info"](path)

        used_percent = sys["percent"](
            used,
            total,
        )

        result = (
            path,
            total,
            used,
            used_percent,
            free,
        )

        if collect:
            return result

        print(
            "Filesystem: {}".format(
                path
            )
        )

        print(
            "Size:       {}".format(
                sys["format_size"](total)
            )
        )

        print(
            "Used:       {} ({}%)".format(
                sys["format_size"](used),
                used_percent,
            )
        )

        print(
            "Free:       {}".format(
                sys["format_size"](free)
            )
        )

        return None

    except Exception as e:
        print(
            "df: {}".format(e)
        )

        return False
