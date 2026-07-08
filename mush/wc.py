__doc__ = """
NAME
    wc - print newline, word, and byte counts

SYNOPSIS
    wc file1 [file2 ...]

DESCRIPTION
    Streams files using mush _fsio and computes:
      - lines
      - words
      - bytes
"""

from mush._fsio import read_chunks

def _count_stream(path):
    lines = 0
    words = 0
    bytes_ = 0

    in_word = False

    for chunk in read_chunks(path):
        bytes_ += len(chunk)

        for b in chunk:
            if b == 10:  # '\n'
                lines += 1

            # whitespace detection (ASCII subset, embedded-safe)
            if b in (32, 9, 10, 13):  # space, tab, newline, CR
                if in_word:
                    words += 1
                    in_word = False
            else:
                in_word = True

    if in_word:
        words += 1

    return lines, words, bytes_

def main(*paths):
    if not paths:
        print("wc: missing file operand")
        return

    total_l = total_w = total_b = 0

    for p in paths:
        try:
            l, w, b = _count_stream(p)
            total_l += l
            total_w += w
            total_b += b

            print("{:>6} {:>6} {:>6} {}".format(l, w, b, p))
        except OSError as e:
            print("wc: {}: {}".format(p, e))

    if len(paths) > 1:
        print("{:>6} {:>6} {:>6} total".format(total_l, total_w, total_b))
