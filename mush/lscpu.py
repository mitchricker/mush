__doc__ = """
NAME
    lscpu - display CPU information

SYNOPSIS
    lscpu()

DESCRIPTION
    Displays CPU and runtime information.
"""

import mush

sysinfo = mush._load_internal("_sys")


def main():
    arch, platform, freq, reset = sysinfo["cpu_info"]()

    lines = []

    lines.append("{:<10} {}".format(
        "arch",
        arch,
    ))

    lines.append("{:<10} {}".format(
        "platform",
        platform,
    ))

    if freq:
        if isinstance(freq, int) and freq >= 1000000:
            freq = "{} MHz".format(
                freq // 1000000,
            )

        lines.append("{:<10} {}".format(
            "freq",
            freq,
        ))

    if reset is not None:
        lines.append("{:<10} {}".format(
            "reset",
            reset,
        ))

    result = "\n".join(lines)

    print(result)

    return lines
