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
        return input(
            "delete {}? [y/N]: ".format(path)
        ).lower() == "y"
    except Exception:
        return False


def _is_dir(path):
    try:
        return bool(os.stat(path)[0] & 0x4000)
    except Exception:
        return False


def _rm_file(path):
    try:
        os.remove(path)
        print("removed:", path)
        return True
    except OSError as e:
        print("rm failed:", path, "->", e)
        return False


def _rm_dir(path, interactive):
    success = True

    try:
        for entry in os.listdir(path):
            full = path + "/" + entry

            if interactive and not _confirm(full):
                continue

            if not _rm(full, True, interactive):
                success = False

        if success:
            os.rmdir(path)
            print("removed dir:", path)

        return success

    except OSError as e:
        print("rmdir failed:", path, "->", e)
        return False


def _rm(path, recursive=False, interactive=False):
    if _is_dir(path):
        if not recursive:
            print("rm: is a directory:", path)
            return False

        return _rm_dir(path, interactive)

    if interactive and not _confirm(path):
        return True

    return _rm_file(path)


def main(*paths, recursive=False, interactive=False):
    if not paths:
        print("usage: rm(path, ...)")
        return False

    success = True

    for path in paths:
        if not _rm(
            path,
            recursive,
            interactive,
        ):
            success = False

    return success
