__doc__ = """
NAME
    free - display memory usage

SYNOPSIS
    free()
    free(collect=True)

DESCRIPTION
    Displays current heap memory status.

    If collect=True, triggers garbage collection before reporting.
"""

import gc

def main(collect=True):
    if collect:
        gc.collect()

    free = None
    alloc = None

    try:
        free = gc.mem_free()
        alloc = gc.mem_alloc()
    except Exception:
        print("free: gc memory info not available")
        return

    total = free + alloc

    usage_pct = (alloc * 100) // total if total else 0

    print("Memory:")
    print("  total: {} bytes".format(total))
    print("  used : {} bytes".format(alloc))
    print("  free : {} bytes".format(free))
    print("  use% : {}%".format(usage_pct))