__doc__ = """
NAME
    runtime - display MicroPython runtime information

SYNOPSIS
    runtime(
        modules=True,
        memory=True,
        tasks=False,
        collect=False,
    )

    runtime("stop", task)

DESCRIPTION
    Displays information about the currently running MicroPython
    runtime, including implementation details, loaded modules,
    memory usage and asyncio tasks.

    Can also stop background asyncio tasks registered by services.

    Returns:

        stop:
            True  - task stopped
            False - task not found

        collect=False:
            None on success
            False on error

        collect=True:
            {
                "version": version,
                "implementation": implementation,
                "modules": modules,
                "memory": memory,
                "tasks": tasks,
            }

            False on error

EXAMPLES
    runtime()

    runtime(
        modules=False
    )

    runtime(
        tasks=True
    )

    runtime(
        collect=True
    )

    runtime(
        "stop",
        "httpd",
    )
"""

import sys
import gc
import mush


def _format_bytes(value):
    if value < 1024:
        return "{} B".format(value)

    if value < 1024 * 1024:
        return "{:.1f} KB".format(
            value / 1024
        )

    return "{:.1f} MB".format(
        value / (1024 * 1024)
    )


def _get_modules():
    return tuple(
        sorted(
            sys.modules.keys()
        )
    )


def _get_memory():
    try:
        gc.collect()

        return (
            gc.mem_alloc(),
            gc.mem_free(),
        )

    except Exception:
        return None


def _get_tasks():
    try:
        runtime = mush._load_internal(
            "_runtime"
        )

        return tuple(
            runtime["tasks"]()
        )

    except Exception:
        return None


def _stop_task(name):
    try:
        runtime = mush._load_internal(
            "_runtime"
        )

        if runtime["stop"](name):
            print(
                "Stopped:",
                name,
            )

            return True

        print(
            "No such task:",
            name,
        )

        return False

    except Exception as e:
        print(
            "runtime:",
            e,
        )

        return False


def _display(data):
    print(
        "MicroPython Runtime"
    )

    print(
        "==================="
    )

    if data["version"]:
        print(
            "Version:",
            data["version"],
        )

    if data["implementation"]:
        print(
            "Implementation:",
            data["implementation"],
        )

    modules = data["modules"]

    if modules is not None:
        print()
        print(
            "Loaded Modules"
        )
        print(
            "=============="
        )

        for module in modules:
            print(
                "    " + module
            )

        print()
        print(
            "Total:",
            len(modules),
        )

    memory = data["memory"]

    if memory:
        print()
        print(
            "Memory"
        )
        print(
            "======"
        )

        alloc, free = memory

        print(
            "    Allocated:",
            _format_bytes(alloc),
        )

        print(
            "    Free:     ",
            _format_bytes(free),
        )

    tasks = data["tasks"]

    if tasks is not None:
        print()
        print(
            "Asyncio Tasks"
        )
        print(
            "============="
        )

        if tasks:
            for task in tasks:
                print(
                    "    " + task
                )

            print()

        else:
            print(
                "    none"
            )

        print(
            "Total:",
            len(tasks),
        )


def main(
    cmd=None,
    *args,
    modules=True,
    memory=True,
    tasks=False,
    collect=False,
):
    if cmd == "stop":

        if not args:
            print(
                "runtime: stop requires task name"
            )

            return False

        return _stop_task(
            args[0]
        )

    try:
        data = {
            "version": None,
            "implementation": None,
            "modules": None,
            "memory": None,
            "tasks": None,
        }

        try:
            data["version"] = (
                sys.version.split()[0]
            )

        except Exception:
            pass

        try:
            data["implementation"] = (
                sys.implementation.name
            )

        except Exception:
            pass

        if modules:
            data["modules"] = _get_modules()

        if memory:
            data["memory"] = _get_memory()

        if tasks:
            data["tasks"] = _get_tasks()

        if collect:
            return data

        _display(data)

        return None

    except Exception as e:
        print(
            "runtime: {}".format(e)
        )

        return False
