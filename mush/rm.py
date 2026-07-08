__doc__ = """
NAME
    rm - remove files or directories

SYNOPSIS
    rm(path, ...)
    rm(path, recursive=True)
    rm(path, recursive=True, interactive=True)

DESCRIPTION
    Removes one or more files or directories.

    Options:
        recursive   - delete directories recursively
        interactive - ask confirmation per file

EXAMPLES
    rm("file.txt")
    rm("file1.txt", "file2.txt", "file3.txt")
    rm("dir", recursive=True)
    rm("dir1", "dir2", recursive=True)
    rm("dir", recursive=True, interactive=True)
"""

import os


def _confirm(path):
    try:
        return input("delete {}? [y/N]: ".format(path)).lower() == "y"
    except Exception:
        return False


def _rm_file(path):
    try:
        os.remove(path)
        print("removed:", path)
    except Exception as e:
        print("rm failed:", path, "->", e)


def _rm_dir(path, interactive):
    try:
        for entry in os.listdir(path):
            full = path + "/" + entry

            if interactive and not _confirm(full):
                continue

            _rm(full, True, interactive)

        os.rmdir(path)
        print("removed dir:", path)

    except Exception as e:
        print("rmdir failed:", path, "->", e)


def _rm(path, recursive=False, interactive=False):
    try:
        is_dir = False
        try:
            is_dir = bool(os.stat(path)[0] & 0x4000)
        except Exception:
            pass

        if is_dir:
            if recursive:
                _rm_dir(path, interactive)
            else:
                print("rm: is a directory:", path)
        else:
            if interactive and not _confirm(path):
                return
            _rm_file(path)

    except Exception as e:
        print("rm error:", path, "->", e)


def main(*paths, recursive=False, interactive=False):
    if not paths:
        print("usage: rm(path, ...)")
        return

    for path in paths:
        _rm(path, recursive, interactive)
