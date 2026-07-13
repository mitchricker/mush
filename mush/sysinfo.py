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
    memory, cpu, uname, fs = sys["summary"](path)

    free, alloc, total = memory
    arch, platform, freq, reset = cpu
    sysname, node, release, version, machine = uname

    lines = []

    lines.append("Mitch's Micro Shell")
    lines.append("----------------")

    if sysname:
        lines.append("System:     {}".format(sysname))
        lines.append("Release:    {}".format(release))
        lines.append("Machine:    {}".format(machine))

    lines.append("")
    lines.append("Platform:   {}".format(platform))
    lines.append("Arch:       {}".format(arch))

    if freq:
        if isinstance(freq, int) and freq >= 1000000:
            freq = "{} MHz".format(freq // 1000000)
        lines.append("CPU:        {}".format(freq))

    if reset is not None:
        lines.append("Reset:      {}".format(reset))

    lines.append("")
    lines.append("Memory:")
    lines.append("  Total:    {}".format(
        sys["format_size"](total)
    ))
    lines.append("  Used:     {}".format(
        sys["format_size"](alloc)
    ))
    lines.append("  Free:     {}".format(
        sys["format_size"](free)
    ))

    if fs:
        block, blocks, blocks_free, total, used, free = fs

        lines.append("")
        lines.append("Filesystem:")
        lines.append("  Total:    {}".format(
            sys["format_size"](total)
        ))
        lines.append(
            "  Used:     {} ({}%)".format(
                sys["format_size"](used),
                sys["percent"](used, total),
            )
        )
        lines.append("  Free:     {}".format(
            sys["format_size"](free)
        ))

    result = "\n".join(lines)

    print(result)

    return result
