__doc__ = """
NAME
    nslookup - query DNS for a hostname or address

SYNOPSIS
    nslookup(host, server="8.8.8.8", collect=False)

DESCRIPTION
    Performs DNS lookups using a DNS server.

    Supports:
        - forward lookup (hostname -> IPv4 addresses)
        - reverse lookup (IPv4 address -> hostname)

    Options:
        server:
            DNS server address.

    Returns:
        collect=False:
            None on success.
            False on error.

        collect=True:
            List of lookup results.

EXAMPLES
    nslookup("example.com")

    nslookup(
        "example.com",
        server="1.1.1.1",
    )

    nslookup(
        "8.8.8.8",
        collect=True,
    )
"""

import random
import mush

net = mush._load_internal("_net")


def _encode_name(name):
    out = b""

    for part in name.split("."):
        out += bytes([len(part)])
        out += part.encode()

    return out + b"\x00"


def _decode_name(data, offset):
    labels = []

    while True:
        length = data[offset]

        if length == 0:
            return ".".join(labels), offset + 1

        if length & 0xc0:
            ptr = (
                (length & 0x3f) << 8
            ) | data[offset + 1]

            label, _ = _decode_name(
                data,
                ptr,
            )

            return ".".join(
                labels + [label]
            ), offset + 2

        offset += 1

        labels.append(
            data[offset:offset + length]
            .decode(
                "utf-8",
                "ignore",
            )
        )

        offset += length


def _dns_query(server, name, qtype):
    ident = random.randint(
        0,
        65535,
    )

    packet = bytearray(
        ident.to_bytes(2, "big")
        + b"\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00"
    )

    packet += _encode_name(name)
    packet += qtype.to_bytes(2, "big")
    packet += b"\x00\x01"

    sock = net["udp_connect"](
        server,
        53,
    )

    try:
        sock.send(packet)
        return sock.recv(512)

    finally:
        net["safe_close"](sock)


def _parse_answers(data):
    answers = []

    offset = 12

    qd = int.from_bytes(
        data[4:6],
        "big",
    )

    an = int.from_bytes(
        data[6:8],
        "big",
    )

    for _ in range(qd):
        _, offset = _decode_name(
            data,
            offset,
        )

        offset += 4

    for _ in range(an):
        _, offset = _decode_name(
            data,
            offset,
        )

        rtype = int.from_bytes(
            data[offset:offset + 2],
            "big",
        )

        offset += 8

        length = int.from_bytes(
            data[offset:offset + 2],
            "big",
        )

        offset += 2

        answers.append(
            (
                rtype,
                data[offset:offset + length],
                offset,
            )
        )

        offset += length

    return answers


def _is_ipv4(value):
    parts = value.split(".")

    if len(parts) != 4:
        return False

    try:
        return all(
            0 <= int(x) <= 255
            for x in parts
        )

    except Exception:
        return False


def main(
    host,
    server="8.8.8.8",
    collect=False,
):
    if not host:
        print(
            "nslookup: missing host"
        )
        return False

    results = []

    try:
        if _is_ipv4(host):
            query = ".".join(
                reversed(
                    host.split(".")
                )
            ) + ".in-addr.arpa"

            data = _dns_query(
                server,
                query,
                12,
            )

            for rtype, _, offset in _parse_answers(data):
                if rtype == 12:
                    name, _ = _decode_name(
                        data,
                        offset,
                    )

                    results.append(name)

        else:
            data = _dns_query(
                server,
                host,
                1,
            )

            for rtype, rdata, _ in _parse_answers(data):
                if (
                    rtype == 1
                    and len(rdata) == 4
                ):
                    results.append(
                        "{}.{}.{}.{}".format(
                            *rdata
                        )
                    )

    except Exception as e:
        print(
            "nslookup: {}: {}".format(
                host,
                e,
            )
        )

        return False

    if collect:
        return results

    for item in results:
        print(item)

    return None
