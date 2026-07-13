__doc__ = """
NAME
    sysinfo - display system summary

SYNOPSIS
    sysinfo()
    sysinfo(path="/")

DESCRIPTION
    Displays system, CPU, memory, and filesystem information.

EXAMPLES
    sysinfo()
    sysinfo("/")
"""
import mush
sys = mush._load_internal("_sys")
def main(path="/"):
    info = sys["summary"](path)
    uname = info["uname"]
    cpu = info["cpu"]
    mem = info["memory"]
    fs = info["filesystem"]
    print("Mitch's Micro Shell")
    print("----------------")
    if uname:
        print("System:     {}".format(uname.get("sysname", "")))
        print("Release:    {}".format(uname.get("release", "")))
        print("Machine:    {}".format(uname.get("machine", "")))
    print()
    print("Platform:   {}".format(cpu.get("platform", "")))
    print("Arch:       {}".format(cpu.get("arch", "")))
    freq = cpu.get("freq")
    if freq:
        if isinstance(freq, int) and freq >= 1000000:
            freq = "{} MHz".format(freq // 1000000)
        print("CPU:        {}".format(freq))
    print()
    print("Memory:")
    print("  Total:    {}".format(
        sys["format_size"](mem["total"])
    ))
    print("  Used:     {}".format(
        sys["format_size"](mem["allocated"])
    ))
    print("  Free:     {}".format(
        sys["format_size"](mem["free"])
    ))
    if fs:
        print()
        print("Filesystem:")
        print("  Total:    {}".format(
            sys["format_size"](fs["total"])
        ))
        print(
            "  Used:     {} ({}%)".format(
                sys["format_size"](fs["used"]),
                sys["percent"](
                    fs["used"],
                    fs["total"],
                ),
            )
        )
        print("  Free:     {}".format(
            sys["format_size"](fs["free"])
        ))
