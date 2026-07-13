__doc__ = """
NAME
    df - display filesystem usage

SYNOPSIS
    df([path="/"])

DESCRIPTION
    Displays filesystem size and usage.

EXAMPLES
    df()
    
    df("/system")
    
    df("/flash")
"""

import mush

sys = mush._load_internal("_sys")

def main(path="/"):
    block, blocks, blocks_free, total, used, free = (
        sys["fs_info"](path)
    )

    used_percent = sys["percent"](used, total)

    print("Filesystem: {}".format(path))
    print("Size:       {}".format(
        sys["format_size"](total)
    ))
    print("Used:       {} ({}%)".format(
        sys["format_size"](used),
        used_percent,
    ))
    print("Free:       {}".format(
        sys["format_size"](free)
    ))

    return (
        path,
        total,
        used,
        used_percent,
        free,
    )
