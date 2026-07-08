__doc__ = """
NAME
    man - display documentation for mush commands

SYNOPSIS
    man()
    man(command)

DESCRIPTION
    Displays the manual page for a mush command.

    With no arguments, prints a list of available commands.

    With a command name, imports that command module,
    displays its documentation, then immediately unloads
    the module and runs garbage collection.

EXAMPLES
    man()
    man("ls")
    man("wifi")
"""

"""
NAME
    man - display documentation for mush commands
SYNOPSIS
    man()
    man(command)
DESCRIPTION
    Displays manual pages for mush commands.
"""
import gc
import sys
import os

def _pad(s, width):
    s = str(s)
    pad = width - len(s)
    if pad < 0:
        pad = 0
    return s + (" " * pad)


def _print_columns(items, cols=3, width=14):
    items = sorted(str(x) for x in items)
    if not items:
        return
    rows = (len(items) + cols - 1) // cols
    for r in range(rows):
        line = ""
        for c in range(cols):
            i = r + c * rows
            if i < len(items):
                line += _pad(items[i], width)
        print(line.rstrip())

def _list_commands():
    try:
        files = os.listdir("mush")
    except Exception:
        return []
    cmds = []
    for f in files:
        if f.endswith(".py") and not f.startswith("_") and f != "__init__.py":
            cmds.append(f[:-3])
    return cmds

def main(command=None):

    if command is None:
        print('Usage: man("command")\n')
        print("Available commands:\n")

        cmds = _list_commands()

        if not cmds:
            print("Unable to enumerate commands.")
            return
        _print_columns(cmds, cols=3, width=14)
        return

    module_name = "mush." + command

    try:
        __import__(module_name)
        mod = sys.modules[module_name]
    except Exception:
        print("{}: command not found".format(command))
        return
    try:
        help_text = getattr(mod, "HELP", None) or getattr(mod, "__doc__", None)

        if help_text:
            print(help_text.strip())
        else:
            print("{}: no manual entry".format(command))
    finally:
        try:
            del sys.modules[module_name]
        except Exception:
            pass
        try:
            del mod
        except Exception:
            pass

        gc.collect()