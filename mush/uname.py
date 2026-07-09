__doc__ = """
NAME
    uname - display system information

SYNOPSIS
    uname()
"""
import mush
sysinfo = mush._load_internal("_sys")
def main():
    info = sysinfo["uname_info"]()
    print("{} {} {} {} {}".format(
        info["sysname"],
        info["nodename"],
        info["release"],
        info["version"],
        info["machine"],
    ))
