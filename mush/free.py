__doc__ = """
NAME
    free - display memory usage

SYNOPSIS
    free()

DESCRIPTION
    Displays MicroPython heap memory usage.

    Returns the formatted output string.
"""
import mush
def main():
    free, alloc, total = mush._load_internal("_sys")["mem_info"]()

    usage_pct = 0
    if total:
        usage_pct = (alloc * 100) // total

    result = (
        "Memory:\n"
        "  total: {} bytes\n"
        "  used : {} bytes\n"
        "  free : {} bytes\n"
        "  use% : {}%"
    ).format(
        total,
        alloc,
        free,
        usage_pct,
    )

    print(result)
    
    return total, alloc, free, usage_pct
