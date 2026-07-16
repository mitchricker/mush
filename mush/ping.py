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
        collect=False:
            None on success
            False on failure

        collect=True:
            (
                sent,
                received,
                [
                    (sequence, milliseconds),
                    ...
                ]
            )

EXAMPLES
    ping("192.168.1.1")

    ping(
        "example.com",
        port=443,
    )

    ping(
        "8.8.8.8",
        port=53,
        count=0,
    )

    ping(
        "example.com",
        collect=True,
    )
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
    if not host:
        print(
            "ping: missing host"
        )
        return False

    if count < 0:
        print(
            "ping: invalid count"
        )
        return False

    if not collect:
        print(
            "TCP PING {}:{}".format(
                host,
                port,
            )
        )
        print()

    results = []

    received = 0
    sent = 0

    try:
        while True:
            if count and sent >= count:
                break

            sequence = sent

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

                received += 1

                if collect:
                    results.append(
                        (
                            sequence,
                            ms,
                        )
                    )

                else:
                    print(
                        "seq={} time={} ms".format(
                            sequence,
                            ms,
                        )
                    )

            except Exception:
                if not collect:
                    print(
                        "seq={} timeout".format(
                            sequence,
                        )
                    )

            finally:
                if sock:
                    net["safe_close"](sock)

            sent += 1

    except KeyboardInterrupt:
        if not collect:
            print(
                "\nping stopped by user"
            )

    if collect:
        return (
            sent,
            received,
            results,
        )

    if not received and sent:
        print()

        print(
            "{} sent, {} received".format(
                sent,
                received,
            )
        )

        return None

    print()

    print(
        "{} sent, {} received".format(
            sent,
            received,
        )
    )

    return None
