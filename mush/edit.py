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
        self.trailing_newline = False
        self.dirty = False
    def load(self, source=None):
        if source is None:
            source = self.path
        self.lines = []
        self.trailing_newline = False
        try:
for item in fsio["iter_lines"](source):
    try:
        line, terminated = item
        self.trailing_newline = terminated
    except Exception:
        line = item
    self.lines.append(line.rstrip(b"\r").decode("utf-8", "ignore"))
        except Exception:
            pass
        if not self.lines:
            self.lines = [""]
        self.dirty = False
    def save(self):
        def writer(f):
            last = len(self.lines) - 1
            for i, line in enumerate(self.lines):
                f.write(line.encode())
                if i < last or self.trailing_newline:
                    f.write(b"\n")
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
        self.trailing_newline = True
        self.dirty = True
    def delete_line(self, row):
        del self.lines[row]
        if not self.lines:
            self.lines = [""]
        self.dirty = True
    def insert_char(self, row, col, char):
        line = self.lines[row]
        self.lines[row] = (
            line[:col] +
            char +
            line[col:]
        )
        self.dirty = True
    def delete_char(self, row, col):
        line = self.lines[row]
        self.lines[row] = (
            line[:col] +
            line[col + 1:]
        )
        self.dirty = True
def _check_recovery(path):
    tmp = path + ".tmp"
    try:
        os.stat(tmp)
    except Exception:
        return None
    try:
        answer = input("Recovery file found: {}\nRecover? [y/N]: ".format(tmp))
        if answer.lower() == "y":
            return tmp
    except Exception:
        pass
    return None
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
    sys.stdout.write(ESC + "[2J" + ESC + "[H")
    for y in range(SCREEN_ROWS):
        n = top + y
        if n < buf.line_count():
            line = buf.get(n)[:SCREEN_COLS]
        else:
            line = ""
        sys.stdout.write("{:<78}\r\n".format(line))
    sys.stdout.write("-" * SCREEN_COLS + "\r\n")
    dirty = " [modified]" if buf.dirty else ""
    sys.stdout.write(
        "{}{} Ln {}/{} Col {} {}".format(
            buf.path,
            dirty,
            row + 1,
            buf.line_count(),
            col + 1,
            message,
        )
    )
    sys.stdout.write(
        "{}[{};{}H".format(
            ESC,
            row - top + 1,
            col + 1,
        )
    )
try:
    sys.stdout.flush()
except Exception:
    pass

def main(path=None):

    if path is None:
        try:
            path = input("Filename: ").strip()
        except Exception:
            path = ""

        if not path:
            path = "untitled.txt"
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
                        answer = input("Unsaved changes. Quit without saving? [y/N]: ")
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
                line = buf.get(row)
                buf.lines[row] = line[:col]
                buf.insert_line(
                    row + 1,
                    line[col:],
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
                    col = len(buf.get(row - 1))
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
        sys.stdout.write(ESC + "[2J" + ESC + "[H")
        try:
            sys.stdout.flush()
        except Exception:
            pass
