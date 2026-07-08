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
import time
import machine
import mush._net as net
NTP_EPOCH = 2208988800
DEFAULT_SERVER = "pool.ntp.org"
def _ntp_time(server, timeout=2000):
    s = net.udp_connect(server, 123, timeout)
    try:
        # NTP request packet
        # LI = 0, VN = 3, Mode = 3 (client)
        packet = bytearray(48)
        packet[0] = 0x1b
        s.send(packet)
        response = s.recv(48)
        if len(response) < 48:
            raise OSError("invalid NTP response")
        # Transmit Timestamp (seconds) starts at byte 40
        seconds = (
            (response[40] << 24) |
            (response[41] << 16) |
            (response[42] << 8) |
            response[43]
        )
        return seconds - NTP_EPOCH
    finally:
        net.safe_close(s)
def _set_clock(timestamp):
    t = time.gmtime(timestamp)
    rtc = machine.RTC()
    rtc.datetime((
        t[0], # year
        t[1], # month
        t[2], # day
        t[6], # weekday
        t[3], # hour
        t[4], # minute
        t[5], # second
        0
    ))
def main(server=DEFAULT_SERVER):
    try:
        print("ntp: contacting {}".format(server))
        timestamp = _ntp_time(server)
        _set_clock(timestamp)
        t = time.localtime()
        print(
            "time set: {:04d}-{:02d}-{:02d} "
            "{:02d}:{:02d}:{:02d}".format(
                t[0], t[1], t[2],
                t[3], t[4], t[5]
            )
        )
    except Exception as e:
        print("ntp: {}".format(e))
