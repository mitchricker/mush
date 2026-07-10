__doc__ = """
NAME
    runtime - display MicroPython runtime information

WARNING
    Do not run with tasks=True if you are not already 
    importing asyncio for other tasks!

SYNOPSIS
    runtime(modules=True, memory=True, tasks=False)

DESCRIPTION
    Displays information about the currently running MicroPython
    runtime, including implementation details, loaded modules,
    memory usage and (optionally) asyncio task information.

EXAMPLES
    runtime()
    runtime(modules=False)
    runtime(tasks=True)
"""
import sys
import gc
def _print_section(title):
    print()
    print(title)
    print("=" * len(title))
def _show_modules():
    _print_section("Loaded Modules")
    modules = sorted(sys.modules.keys())
    for module in modules:
        print("    " + module)
    print()
    print("Total:", len(modules))
def _show_memory():
    _print_section("Memory")
    try:
        gc.collect()
        print("    Allocated:",
              _format_bytes(gc.mem_alloc()))
        print("    Free:     ",
              _format_bytes(gc.mem_free()))
    except AttributeError:
        print("    unavailable")
def _show_tasks():
    _print_section("Asyncio Tasks")
    try:
        import asyncio
        tasks = asyncio.all_tasks()
        for task in tasks:
            print("    ", task)
        print()
        print("Total:", len(tasks))
    except Exception:
        print("    asyncio unavailable")
def _format_bytes(value):
    if value < 1024:
        return "{} B".format(value)
    if value < 1024 * 1024:
        return "{:.1f} KB".format(value / 1024)
    return "{:.1f} MB".format(value / (1024 * 1024))
def main(modules=True, memory=True, tasks=False):
    print("MicroPython Runtime")
    try:
        print("Version:",
              sys.version.split()[0])
    except Exception:
        pass
    try:
        print("Implementation:",
              sys.implementation.name)
    except Exception:
        pass
    if modules:
        _show_modules()
    if memory:
        _show_memory()
    if tasks:
        _show_tasks()
