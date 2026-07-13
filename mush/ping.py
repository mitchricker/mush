__doc__ = """
NAME
    ping - TCP connectivity test

SYNOPSIS
    ping(host, port=80, count=4, timeout=1000, collect=False)

DESCRIPTION
    Measures TCP connect latency by timing socket
    connection establishment.

    This is NOT ICMP ping. It tests TCP reachability.

    Returns:
        {
            "sent": count,
            "received": successful,
            "results": [(sequence, milliseconds), ...]
        }

    With collect=False, results are printed and only the
    summary tuple is returned.

EXAMPLES
    ping("192.168.1.1")

    ping("example.com", port=443)

    ping("8.8.8.8", port=53, count=0)
"""

import time
import mush

net = mush._load_internal("_net")


def main(
    host,
    port=80,
    count=4,
    timeout=1000,
    collect=False,
):
    if not collect:
        print(
            "TCP PING {}:{}".format(
                host,
                port,
            )
        )
        print()

    results = [] if collect else None

    ok = 0
    sent = 0

    try:
        while True:
            if count and sent >= count:
                break

            start = time.ticks_ms()
            sock = None

            try:
                sock = net["tcp_connect"](
                    host,
                    port,
                    timeout,
                )

                ms = time.ticks_diff(
                    time.ticks_ms(),
                    start,
                )

                ok += 1

                if collect:
                    results.append(
                        (sent, ms)
                    )
                else:
                    print(
                        "seq={} time={} ms".format(
                            sent,
                            ms,
                        )
                    )

            except Exception:
                if not collect:
                    print(
                        "seq={} timeout".format(
                            sent
                        )
                    )

            finally:
                if sock:
                    net["safe_close"](sock)

            sent += 1

    except KeyboardInterrupt:
        if not collect:
            print("\nping stopped by user")

    if collect:
        return (
            sent,
            ok,
            results,
        )

    print()
    print(
        "{} sent, {} received".format(
            sent,
            ok,
        )
    )

    return (
        sent,
        ok,
    )
