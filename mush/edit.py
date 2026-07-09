__doc__ = """
NAME
    edit - simple terminal text editor

SYNOPSIS
    edit(file)

DESCRIPTION
    Minimal full-screen text editor for MicroPython.

KEYS
    Arrow keys       Move cursor
    Home / End       Line start/end
    Page Up/Down     Scroll
    Enter            Split line
    Backspace        Delete
    Ctrl-S           Save
    Ctrl-Q           Quit
    Ctrl-L           Redraw

EXAMPLES
    edit("boot.py")
"""
import sys
import os
import mush
fsio = mush._load_internal("_fsio")
ESC = "\x1b"
CTRL_S = "\x13"
CTRL_Q = "\x11"
CTRL_L = "\x0c"
SCREEN_ROWS = 20
SCREEN_COLS = 78
class FileBuffer:
    def __init__(self, path):
        self.path = path
        self.lines = []
        self.dirty = False
    def load(self, source=None):
        if source is None:
            source = self.path
        self.lines = []
        try:
            for line in fsio["iter_lines"](source):
                self.lines.append(
                    line.decode("utf-8", "ignore")
                )
        except Exception:
            pass
        if not self.lines:
            self.lines = [""]
        self.dirty = False
    def save(self):
        def writer(f):
            for line in self.lines:
                f.write(
                    (line + "\n").encode()
                )
        fsio["atomic_write"](
            self.path,
            writer,
        )
        self.dirty = False
    def line_count(self):
        return len(self.lines)
    def get(self, row):
        return self.lines[row]
    def insert_line(self, row, text=""):
        self.lines.insert(row, text)
        self.dirty = True
    def delete_line(self, row):
        del self.lines[row]
        if not self.lines:
            self.lines = [""]
        self.dirty = True
    def insert_char(self, row, col, char):
        s = self.lines[row]
        self.lines[row] = (
            s[:col] +
            char +
            s[col:]
        )
        self.dirty = True
    def delete_char(self, row, col):
        s = self.lines[row]
        self.lines[row] = (
            s[:col] +
            s[col + 1:]
        )
        self.dirty = True
def _check_recovery(path):
    tmp = path + ".tmp"
    try:
        os.stat(tmp)
    except Exception:
        return None
    try:
        answer = input(
            "Recovery file found: {}\nRecover? [y/N]: ".format(tmp)
        )
        if answer.lower() == "y":
            return tmp
    except Exception:
        pass
    return None
def _clear():
    print(
        ESC + "[2J" + ESC + "[H",
        end="",
    )
def _move(row, col):
    print(
        "{}[{};{}H".format(
            ESC,
            row,
            col,
        ),
        end="",
    )
def _read_key():
    c = sys.stdin.read(1)
    if c != ESC:
        return c
    seq = sys.stdin.read(2)
    keys = {
        "[A": "UP",
        "[B": "DOWN",
        "[C": "RIGHT",
        "[D": "LEFT",
        "[H": "HOME",
        "[F": "END",
    }
    if seq in keys:
        return keys[seq]
    if seq == "[5":
        sys.stdin.read(1)
        return "PGUP"
    if seq == "[6":
        sys.stdin.read(1)
        return "PGDN"
    return ""
def _draw(buf, row, col, top, message=""):
    _clear()
    for y in range(SCREEN_ROWS):
        n = top + y
        if n < buf.line_count():
            print(
                "{:<78}".format(
                    buf.get(n)[:SCREEN_COLS]
                )
            )
        else:
            print("")
    print("-" * SCREEN_COLS)
    dirty = " [modified]" if buf.dirty else ""
    print(
        "{}{} Ln {}/{} Col {} {}".format(
            buf.path,
            dirty,
            row + 1,
            buf.line_count(),
            col + 1,
            message,
        )
    )
    _move(
        row - top + 1,
        col + 1,
    )
def main(path):
    recovery = _check_recovery(path)
    buf = FileBuffer(path)
    if recovery:
        buf.load(recovery)
        buf.dirty = True
    else:
        buf.load()
    row = 0
    col = 0
    top = 0
    message = ""
    try:
        while True:
            if row < top:
                top = row
            if row >= top + SCREEN_ROWS:
                top = row - SCREEN_ROWS + 1
            _draw(
                buf,
                row,
                col,
                top,
                message,
            )
            message = ""
            key = _read_key()
            if key == CTRL_S:
                try:
                    buf.save()
                    message = "saved"
                except Exception as e:
                    message = "save failed: {}".format(e)
            elif key == CTRL_L:
                continue
            elif key == CTRL_Q:
                if buf.dirty:
                    try:
                        answer = input(
                            "Unsaved changes. Quit without saving? [y/N]: "
                        )
                        if answer.lower() != "y":
                            continue
                    except Exception:
                        continue
                break
            elif key == "UP":
                if row:
                    row -= 1
                    col = min(
                        col,
                        len(buf.get(row)),
                    )
            elif key == "DOWN":
                if row < buf.line_count() - 1:
                    row += 1
                    col = min(
                        col,
                        len(buf.get(row)),
                    )
            elif key == "LEFT":
                if col:
                    col -= 1
            elif key == "RIGHT":
                if col < len(buf.get(row)):
                    col += 1
            elif key == "HOME":
                col = 0
            elif key == "END":
                col = len(buf.get(row))
            elif key == "PGUP":
                row = max(
                    0,
                    row - SCREEN_ROWS,
                )
            elif key == "PGDN":
                row = min(
                    buf.line_count() - 1,
                    row + SCREEN_ROWS,
                )
            elif key in ("\r", "\n"):
                s = buf.get(row)
                buf.lines[row] = s[:col]
                buf.insert_line(
                    row + 1,
                    s[col:],
                )
                row += 1
                col = 0
            elif key in ("\b", "\x7f"):
                if col:
                    buf.delete_char(
                        row,
                        col - 1,
                    )
                    col -= 1
                elif row:
                    col = len(
                        buf.get(row - 1)
                    )
                    buf.lines[row - 1] += buf.get(row)
                    buf.delete_line(row)
                    row -= 1
            elif len(key) == 1 and ord(key) >= 32:
                buf.insert_char(
                    row,
                    col,
                    key,
                )
                col += 1
    finally:
        _clear()
