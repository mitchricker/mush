import gc
import os
import sys
try:
    import machine
except ImportError:
    machine = None
def mem_info():
    gc.collect()
    free = gc.mem_free()
    alloc = gc.mem_alloc()
    return {
        "free": free,
        "allocated": alloc,
        "total": free + alloc,
    }
def fs_info(path="/"):
    s = os.statvfs(path)
    block = s[0]
    total_blocks = s[2]
    free_blocks = s[3]
    total = block * total_blocks
    free = block * free_blocks
    return {
        "block_size": block,
        "blocks": total_blocks,
        "blocks_free": free_blocks,
        "total": total,
        "used": total - free,
        "free": free,
    }
def cpu_info():
    info = {
        "arch": sys.implementation.name,
        "platform": sys.platform,
        "freq": None,
        "reset": None,
    }
    if machine:
        try:
            info["freq"] = machine.freq()
        except Exception:
            pass
        try:
            info["reset"] = machine.reset_cause()
        except Exception:
            pass
    return info
def uname_info():
    try:
        u = os.uname()
        return {
            "sysname": u.sysname,
            "nodename": getattr(u, "nodename", ""),
            "release": u.release,
            "version": u.version,
            "machine": u.machine,
        }
    except Exception:
        return {
            "sysname": "",
            "nodename": "",
            "release": "",
            "version": "",
            "machine": "",
        }
def format_size(size):
    units = (
        "B",
        "KiB",
        "MiB",
        "GiB",
    )
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            if unit == "B":
                return "%d %s" % (int(value), unit)
            return "%.1f %s" % (value, unit)
        value /= 1024
def percent(used, total):
    if total <= 0:
        return 0
    return int((used * 100) / total)
def summary(path="/"):
    info = {
        "memory": mem_info(),
        "cpu": cpu_info(),
        "uname": uname_info(),
    }
    try:
        info["filesystem"] = fs_info(path)
    except Exception:
        info["filesystem"] = None
    return info
