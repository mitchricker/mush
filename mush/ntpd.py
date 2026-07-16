__doc__ = """
NAME
    ntpd - Network Time Protocol daemon

SYNOPSIS
    ntpd()
    ntpd(server, interval=3600)

DESCRIPTION
    Periodically synchronizes the system clock.

    Runs as a background asyncio task.

    Returns:
        True  - daemon running
        False - failed to start

EXAMPLES
    ntpd()

    ntpd("time.google.com",600)
"""

import asyncio
import mush

ntp = mush._load_internal("_ntp")
runtime = mush._load_internal("_runtime")


async def _run(server, interval):
    try:
        while True:
            try:
                ntp["sync"](server)

            except Exception as e:
                print(
                    "ntpd:",
                    e,
                )

            await asyncio.sleep(interval)

    finally:
        runtime["unregister"](
            "ntpd"
        )


def main(
    server=ntp["DEFAULT_SERVER"],
    interval=3600,
):
    try:
        if "ntpd" in runtime["tasks"]():
            return True

        task = asyncio.create_task(
            _run(
                server,
                interval,
            )
        )

        runtime["register"](
            "ntpd",
            task,
        )

        return True

    except Exception as e:
        print(
            "ntpd:",
            e,
        )

        return False
