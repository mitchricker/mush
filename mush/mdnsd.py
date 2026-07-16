__doc__ = """
NAME
    mdnsd - multicast DNS daemon

SYNOPSIS
    mdnsd()
    mdnsd(name)

DESCRIPTION
    Advertises the board hostname using
    multicast DNS.

    The default hostname is mush.

    Returns:
        True  - daemon running
        False - failed to start

EXAMPLES
    mdnsd()

    mdnsd("sensor")
"""

import asyncio
import socket
import network
import mush

runtime = mush._load_internal("_runtime")

DEFAULT_NAME = "mush"

GROUP = "224.0.0.251"
PORT = 5353


def _encode_name(name):
    out = b""

    for part in name.split("."):
        out += bytes([len(part)])
        out += part.encode()

    return out + b"\0"


def _query_name(data):
    try:
        pos = 12
        parts = []

        while True:
            length = data[pos]
            pos += 1

            if length == 0:
                break

            parts.append(
                data[pos:pos + length].decode()
            )

            pos += length

        return ".".join(parts)

    except Exception:
        return None


def _answer(name, ip):
    packet = bytearray()

    packet += b"\x00\x00"
    packet += b"\x84\x00"
    packet += b"\x00\x00"
    packet += b"\x00\x01"
    packet += b"\x00\x00"
    packet += b"\x00\x00"
    packet += b"\x00\x00"

    packet += _encode_name(name)

    packet += b"\x00\x01"
    packet += b"\x00\x01"
    packet += b"\x00\x00\x00\x78"
    packet += b"\x00\x04"

    packet += bytes(
        int(x)
        for x in ip.split(".")
    )

    return packet


def _ip():
    wlan = network.WLAN(
        network.STA_IF
    )

    if wlan.active():
        return wlan.ifconfig()[0]

    return None


def _socket():
    s = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM,
    )

    s.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1,
    )

    s.bind(
        (
            "0.0.0.0",
            PORT,
        )
    )

    mreq = (
        socket.inet_aton(GROUP)
        +
        socket.inet_aton("0.0.0.0")
    )

    s.setsockopt(
        socket.IPPROTO_IP,
        socket.IP_ADD_MEMBERSHIP,
        mreq,
    )

    s.settimeout(0)

    return s


async def _run(name):
    sock = None

    try:
        sock = _socket()

        hostname = name + ".local"

        print(
            "mdnsd: {}".format(
                hostname
            )
        )

        while True:
            try:
                data, addr = sock.recvfrom(
                    512
                )

            except Exception:
                await asyncio.sleep(0)
                continue

            if _query_name(data) != hostname:
                continue

            ip = _ip()

            if ip:
                sock.sendto(
                    _answer(
                        hostname,
                        ip,
                    ),
                    addr,
                )

            await asyncio.sleep(0)

    finally:
        if sock:
            sock.close()

        runtime["unregister"](
            "mdnsd"
        )


def main(
    name=DEFAULT_NAME,
):
    try:
        if "mdnsd" in runtime["tasks"]():
            return True

        task = asyncio.create_task(
            _run(name)
        )

        runtime["register"](
            "mdnsd",
            task,
        )

        return True

    except Exception as e:
        print(
            "mdnsd:",
            e,
        )

        return False
