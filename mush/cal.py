__doc__ = """
NAME
    cal - display a calendar

SYNOPSIS
    cal()
    cal(year)
    cal(year, month)

DESCRIPTION
    Displays a calendar.

    With no arguments:
        Shows the current month.

    With one argument:
        Shows the requested year.

    With two arguments:
        Shows the requested month.

EXAMPLES
    cal()
    cal(2026)
    cal(2026, 7)
"""

import time

import mush

fsio = mush._load_internal("_fsio")


_MONTHS = (
    "January", "February", "March",
    "April", "May", "June",
    "July", "August", "September",
    "October", "November", "December",
)

_DAYS = (
    "Su", "Mo", "Tu", "We",
    "Th", "Fr", "Sa",
)


def _leap(year):
    if year % 400 == 0:
        return True

    if year % 100 == 0:
        return False

    return year % 4 == 0


def _days_in_month(year, month):
    days = (
        31, 28, 31, 30,
        31, 30, 31, 31,
        30, 31, 30, 31,
    )

    if month == 2 and _leap(year):
        return 29

    return days[month - 1]


def _weekday(year, month, day=1):
    table = (
        0, 3, 2, 5,
        0, 3, 5, 1,
        4, 6, 2, 4,
    )

    if month < 3:
        year -= 1

    return (
        year
        + year // 4
        - year // 100
        + year // 400
        + table[month - 1]
        + day
    ) % 7


def _print_month(write, year, month):
    write(
        "{}\n".format(
            "{} {}".format(
                _MONTHS[month - 1],
                year,
            ).center(20)
        )
    )

    write(
        "{}\n".format(
            " ".join(
                "{:>2}".format(day)
                for day in _DAYS
            )
        )
    )

    first = _weekday(year, month)
    days = _days_in_month(year, month)

    line = "   " * first
    column = first

    for day in range(1, days + 1):
        line += "{:>2} ".format(day)
        column += 1

        if column == 7:
            write(line.rstrip() + "\n")
            line = ""
            column = 0

    if line:
        write(line.rstrip() + "\n")


def _print_year(write, year):
    for month in range(1, 13):
        _print_month(write, year, month)

        if month != 12:
            write("\n")


def main(year=None, month=None, out=None, collect=False):
    write, close, result = fsio["output"](
        out=out,
        collect=collect,
    )

    try:
        if year is None:
            now = time.localtime()
            year = now[0]
            month = now[1]

        elif month is None:
            _print_year(write, year)
            return result()

        if month < 1 or month > 12:
            print("cal: invalid month")
            return False

        _print_month(write, year, month)

    finally:
        close()

    return result()
