__doc__ = """
NAME
    lscpu - display CPU information

SYNOPSIS
    lscpu()
"""
import mush
sysinfo = mush._load_internal("_sys")
def main():
    info = sysinfo["cpu_info"]()
    for key, value in info.items():
        print("{:<10} {}".format(key, value))
