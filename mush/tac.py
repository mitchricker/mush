__doc__ = """
NAME
    tac - concatenate and print files in reverse

SYNOPSIS
    tac(file)

DESCRIPTION
    Prints file lines in reverse order.

EXAMPLES
    tac("log.txt")
    tac("log.txt", collect=True)
"""
import mush
fsio = mush._load_internal("_fsio")
def _print_line(line):
    try:
        print(line.decode("utf-8", "ignore"))
    except Exception:
        print(line)
def main(path):
    try:
        for line in fsio["iter_lines_reverse"](path):
            write(line)
            write(b"\n")
    except OSError as e:
        print(
            "tac: {}: {}".format(
                path,
                e,
            )
        )

        return False

    finally:
        close()

    return result()
