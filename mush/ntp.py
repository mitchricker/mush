__doc__="""
NAME
    ntp - synchronize clock using Network Time Protocol

SYNOPSIS
    ntp()
    ntp(server)

DESCRIPTION
    Synchronizes the system clock using SNTP.

    Default server:
        pool.ntp.org

EXAMPLES
    ntp()
    ntp("time.google.com")
"""
import machine
import mush
ntp=mush._load_internal("_ntp")
def main(server=ntp["DEFAULT_SERVER"]):
    try:
        print(
            "ntp: contacting {}".format(
                server
            )
        )
        ntp["sync"](server)
        t=machine.RTC().datetime()
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
        print("ntp:",e)
