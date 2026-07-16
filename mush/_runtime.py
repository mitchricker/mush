"""
Internal runtime task registry.

Provides:
    register()
    unregister()
    tasks()
    stop()

Used by background services to track asyncio tasks.

Functions:

    register(name, task)

        Register a task by name.


    unregister(name)

        Remove a registered task.


    tasks()

        Return registered task names as a tuple.


    stop(name)

        Cancel and remove a registered task.

        Returns:
            True if stopped
            False if not found
"""
_tasks = {}


def register(name, task):
    _tasks[name] = task


def unregister(name):
    try:
        del _tasks[name]
    except KeyError:
        pass


def tasks():
    return tuple(_tasks.keys())


def stop(name):
    task = _tasks.get(name)

    if not task:
        return False

    try:
        task.cancel()

    except Exception:
        pass

    del _tasks[name]

    return True
