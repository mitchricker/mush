__doc__ = """
NAME
    lscpu - display CPU information

SYNOPSIS
    lscpu(collect=False)

DESCRIPTION
    Displays CPU and runtime information.

    Returns:
        collect=True:
            (
                architecture,
                platform,
                frequency,
                reset cause,
            )

        collect=False:
            None on success
            False on failure

EXAMPLES
    lscpu()

    lscpu(collect=True)
"""

import mush

sysinfo = mush._load_internal("_sys")


def main(collect=False):
    try:
        arch, platform, freq, reset = (
            sysinfo["cpu_info"]()
        )

        result = (
            arch,
            platform,
            freq,
            reset,
        )

        if collect:
            return result

        lines = []

        lines.append(
            "{:<10} {}".format(
                "arch",
                arch,
            )
        )

        lines.append(
            "{:<10} {}".format(
                "platform",
                platform,
            )
        )

        if freq:
            display_freq = freq

            if (
                isinstance(freq, int)
                and freq >= 1000000
            ):
                display_freq = (
                    "{} MHz".format(
                        freq // 1000000
                    )
                )

            lines.append(
                "{:<10} {}".format(
                    "freq",
                    display_freq,
                )
            )

        if reset is not None:
            lines.append(
                "{:<10} {}".format(
                    "reset",
                    reset,
                )
            )

        print(
            "\n".join(lines)
        )

        return None

    except Exception as e:
        print(
            "lscpu: {}".format(e)
        )

        return False
