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
import os
import mush

def _pad(s, width):
    s = str(s)
    return s + (" " * max(0, width - len(s)))

def _print_columns(items, cols=3, width=14):
    items = sorted(items)
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
        files = os.listdir(mush._ROOT)
    except Exception:
        return []

    cmds = []

    for f in files:
        if (
            f.endswith(".py")
            and not f.startswith("_")
            and f != "__init__.py"
        ):
            cmds.append(f[:-3])

    return cmds

def _load_doc(command):
    path = mush._ROOT + "/" + command + ".py"

    try:
        f = open(path)
        source = f.read()
        f.close()
    except Exception:
        return None

    module = {}

    try:
        exec(source, module)
    except Exception:
        return None

    return module.get("__doc__")

def main(command=None):
    if command is None:
        print('Usage: man("command")\n')
        print("Available commands:\n")

        cmds = _list_commands()

        if cmds:
            _print_columns(cmds)
        else:
            print("Unable to enumerate commands.")

        return

    help_text = _load_doc(command)

    if help_text:
        print(help_text.strip())
    else:
        print("{}: command not found".format(command))
