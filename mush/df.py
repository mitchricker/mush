__doc__ = """
NAME
    df - display filesystem usage

SYNOPSIS
    df([path="/"])

DESCRIPTION
    Displays filesystem size and usage.
"""

import mush


def main(path="/"):
    block, blocks, blocks_free, total, used, free = (
        mush._load_internal("_sys")["fs_info"](path)
    )

    result = (
        "Filesystem: {}\n"
        "Size:       {}\n"
        "Used:       {} ({}%)\n"
        "Free:       {}"
    ).format(
        path,
        mush._load_internal("_sys")["format_size"](total),
        mush._load_internal("_sys")["format_size"](used),
        mush._load_internal("_sys")["percent"](used, total),
        mush._load_internal("_sys")["format_size"](free),
    )

    print(result)

    return result
