import gc
import os
import sys

_UNITS = (
    "B",
    "KiB",
    "MiB",
    "GiB",
)

def mem_info():
    gc.collect()
    free = gc.mem_free()
    alloc = gc.mem_alloc()
    return free, alloc, free + alloc

def fs_info(path="/"):
    s = os.statvfs(path)

    block = s[0]
    total_blocks = s[2]
    free_blocks = s[3]

    total = block * total_blocks
    free = block * free_blocks

    return (
        block,
        total_blocks,
        free_blocks,
        total,
        total - free,
        free,
    )

def cpu_info():
    freq = None
    reset = None

    try:
        import machine

        try:
            freq = machine.freq()
        except Exception:
            pass

        try:
            reset = machine.reset_cause()
        except Exception:
            pass

    except ImportError:
        pass

    return (
        sys.implementation.name,
        sys.platform,
        freq,
        reset,
    )

def uname_info():
    try:
        u = os.uname()

        return (
            u.sysname,
            getattr(u, "nodename", ""),
            u.release,
            u.version,
            u.machine,
        )

    except Exception:
        return (
            "",
            "",
            "",
            "",
            "",
        )

def format_size(size):
    value = size

    for unit in _UNITS:
        if value < 1024 or unit == _UNITS[-1]:
            if unit == "B":
                return "{} {}".format(value, unit)

            return "{} {}" .format(
                round(value, 1),
                unit,
            )

        value /= 1024

def percent(used, total):
    if total <= 0:
        return 0

    return (used * 100) // total

def summary(path="/"):
    try:
        filesystem = fs_info(path)
    except Exception:
        filesystem = None

    return (
        mem_info(),
        cpu_info(),
        uname_info(),
        filesystem,
    )