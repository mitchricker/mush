__doc__ = """
NAME
    df - display filesystem usage

SYNOPSIS
    df(path="/")
"""
import mush
sysinfo = mush._load_internal("_sys")
def main(path="/"):
    fs = sysinfo["fs_info"](path)
    print("Filesystem: {}".format(path))
    print(
        "Size:       {}".format(
            sysinfo["format_size"](fs["total"])
        )
    )
    print(
        "Used:       {} ({}%)".format(
            sysinfo["format_size"](fs["used"]),
            sysinfo["percent"](
                fs["used"],
                fs["total"],
            ),
        )
    )
    print(
        "Free:       {}".format(
            sysinfo["format_size"](fs["free"])
        )
    )
