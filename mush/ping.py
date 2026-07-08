__doc__ = """
NAME
    ping - TCP connectivity test

SYNOPSIS
    ping(host)
    ping(host, port=80, count=4, timeout=1000)

DESCRIPTION
    Measures TCP connect latency by timing socket
    connection establishment.

    This is NOT ICMP ping. It tests TCP reachability.

    If count=0, ping runs indefinitely until interrupted.

EXAMPLES
    ping("192.168.1.1")

    ping("example.com", port=443)

    # Test a slow or unreachable host with a short timeout
    ping("10.255.255.1", port=80, timeout=200)

    # Infinite monitoring mode
    ping("8.8.8.8", port=53, count=0)
"""

import time
import mush._net as net


def main(host, port=80, count=4, timeout=1000):
    print("TCP PING {}:{}".format(host, port))
    print()

    ok = 0
    i = 0

    try:
        while True:
            if count and i >= count:
                break

            start = time.ticks_ms()
            sock = None

            try:
                sock = net.tcp_connect(host, port, timeout)
                ms = time.ticks_diff(time.ticks_ms(), start)

                print("seq={} time={} ms".format(i, ms))
                ok += 1

            except Exception:
                print("seq={} timeout".format(i))

            finally:
                if sock:
                    net.safe_close(sock)

            i += 1

    except KeyboardInterrupt:
        print("\nping stopped by user")

    print()
    print("{} sent, {} received".format(i, ok))