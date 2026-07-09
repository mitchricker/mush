__doc__ = """
NAME
    ntp - synchronize clock using Network Time Protocol

SYNOPSIS
    ntp()
    ntp(server)

DESCRIPTION
    Synchronizes the system clock using SNTP.

    Uses UDP port 123.

    Default server:
        pool.ntp.org

EXAMPLES
    ntp()
    ntp("time.google.com")
"""
import machine
import mush
net = mush._load_internal("_net")
NTP_EPOCH = 2208988800
DEFAULT_SERVER = "pool.ntp.org"
def _ntp_time(server, timeout=2000):
    s = net["udp_connect"](server, 123, timeout)
    try:
        packet = bytearray(48)
        # LI=0, VN=3, Mode=3 (client)
        packet[0] = 0x1b
        s.send(packet)
        response = s.recv(48)
        if len(response) < 48:
            raise OSError("invalid NTP response")
        seconds = (
            (response[40] << 24)
            |
            (response[41] << 16)
            |
            (response[42] << 8)
            |
            response[43]
        )
        return seconds - NTP_EPOCH
    finally:
        net["safe_close"](s)
def _unix_to_datetime(timestamp):
    days = timestamp // 86400
    seconds = timestamp % 86400
    year = 1970
    while True:
        leap = (
            year % 4 == 0 and
            (year % 100 != 0 or year % 400 == 0)
        )
        year_days = 366 if leap else 365
        if days < year_days:
            break
        days -= year_days
        year += 1
    leap = (
        year % 4 == 0 and
        (year % 100 != 0 or year % 400 == 0)
    )
    months = [
        31,
        29 if leap else 28,
        31,
        30,
        31,
        30,
        31,
        31,
        30,
        31,
        30,
        31,
    ]
    month = 1
    for length in months:
        if days < length:
            break
        days -= length
        month += 1
    day = days + 1
    hour = seconds // 3600
    seconds %= 3600
    minute = seconds // 60
    second = seconds % 60
    return (
        year,
        month,
        day,
        hour,
        minute,
        second,
    )
def _set_clock(timestamp):
    year, month, day, hour, minute, second = _unix_to_datetime(timestamp)
    rtc = machine.RTC()
    rtc.datetime((
        year,
        month,
        day,
        0,
        hour,
        minute,
        second,
        0,
    ))
def main(server=DEFAULT_SERVER):
    try:
        print("ntp: contacting {}".format(server))
        timestamp = _ntp_time(server)
        _set_clock(timestamp)
        t = machine.RTC().datetime()
        print(
            "time set: {:04d}-{:02d}-{:02d} "
            "{:02d}:{:02d}:{:02d}".format(
                t[0],
                t[1],
                t[2],
                t[4],
                t[5],
                t[6],
            )
        )
    except Exception as e:
        print("ntp: {}".format(e))
