__doc__ = """
NAME
    lscpu - display CPU information

SYNOPSIS
    lscpu()
"""
import mush._sys as sysinfo
def main():
    info = sysinfo.cpu_info()
    for key, value in info.items():
        print(
            "{:<10} {}".format(
                key,
                value,
            )
        )
