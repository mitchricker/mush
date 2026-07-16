__doc__ = """
NAME
    free - display memory usage

SYNOPSIS
    free(collect=False)

DESCRIPTION
    Displays MicroPython heap memory usage.

    Runs garbage collection before measuring by default.

    Returns:

        collect=False:
            None on success
            False on error

        collect=True:
            (
                total memory,
                used memory,
                free memory,
                usage percentage
            )

            False on error

OPTIONS

    gc:
        Run gc.collect() before measuring.
        Default: True

EXAMPLES
    free()

    free(collect=True)

"""

import gc
import mush


def main(
    collect=False,
):
    try:

        free, alloc, total = (
            mush._load_internal("_sys")["mem_info"]()
        )

        usage_pct = 0

        if total:
            usage_pct = (
                alloc * 100
            ) // total

        result = (
            total,
            alloc,
            free,
            usage_pct,
        )

        if collect:
            return result

        print(
            "Memory:\n"
            "  total: {} bytes\n"
            "  used : {} bytes\n"
            "  free : {} bytes\n"
            "  use% : {}%"
            .format(
                total,
                alloc,
                free,
                usage_pct,
            )
        )

        return None

    except Exception as e:
        print(
            "free: {}".format(e)
        )

        return False
