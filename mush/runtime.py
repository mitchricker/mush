__doc__="""
NAME
    runtime - display MicroPython runtime information

SYNOPSIS
    runtime(modules=True,memory=True,tasks=False)
    runtime("stop",task)

DESCRIPTION
    Displays information about the currently running MicroPython
    runtime, including implementation details, loaded modules,
    memory usage and asyncio tasks.

    Can also stop background asyncio tasks registered by services.

EXAMPLES
    runtime()
    runtime(modules=False)
    runtime(tasks=True)
    runtime("stop","httpd")
"""
import sys
import gc
import mush
def _print_section(title):
    print()
    print(title)
    print("=" * len(title))
def _show_modules():
    _print_section("Loaded Modules")
    modules=sorted(sys.modules.keys())
    for module in modules:
        print("    "+module)
    print()
    print("Total:",len(modules))
def _format_bytes(value):
    if value<1024:
        return "{} B".format(value)
    if value<1024*1024:
        return "{:.1f} KB".format(value/1024)
    return "{:.1f} MB".format(value/(1024*1024))
def _show_memory():
    _print_section("Memory")
    try:
        gc.collect()
        print(
            "    Allocated:",
            _format_bytes(gc.mem_alloc()),
        )
        print(
            "    Free:     ",
            _format_bytes(gc.mem_free()),
        )
    except AttributeError:
        print("    unavailable")
def _show_tasks():
    _print_section("Asyncio Tasks")
    try:
        runtime=mush._load_internal(
            "_runtime"
        )
        tasks=runtime["tasks"]()
        if not tasks:
            print("    none")
            return
        for name in tasks:
            print("    "+name)
        print()
        print("Total:",len(tasks))
    except Exception:
        print("    unavailable")
def _stop_task(name):
    try:
        runtime=mush._load_internal(
            "_runtime"
        )
        if runtime["stop"](name):
            print("Stopped:",name)
        else:
            print(
                "No such task:",
                name,
            )
    except Exception as e:
        print(
            "runtime:",
            e,
        )
def main(cmd=None,*args,modules=True,memory=True,tasks=False):
    if cmd=="stop":
        if not args:
            print(
                "runtime: stop requires task name"
            )
            return
        _stop_task(args[0])
        return
    print("MicroPython Runtime")
    try:
        print(
            "Version:",
            sys.version.split()[0],
        )
    except Exception:
        pass
    try:
        print(
            "Implementation:",
            sys.implementation.name,
        )
    except Exception:
        pass
    if modules:
        _show_modules()
    if memory:
        _show_memory()
    if tasks:
        _show_tasks()
