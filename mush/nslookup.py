__doc__ = """
NAME
    nslookup - query DNS for a hostname or address

SYNOPSIS
    nslookup(host)

DESCRIPTION
    Performs DNS lookups.

EXAMPLES
    nslookup("example.com")
    nslookup("8.8.8.8")
"""

import random
import socket

import mush._net as net


DNS_SERVER = "8.8.8.8"


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
            offset += 1
            break

        # DNS compression pointer
        if length & 0xC0:
            ptr = ((length & 0x3F) << 8) | data[offset + 1]
            label, _ = _decode_name(data, ptr)
            labels.append(label)
            offset += 2
            break

        offset += 1
        labels.append(
            data[offset:offset + length].decode("utf-8", "ignore")
        )
        offset += length

    return ".".join(labels), offset


def _dns_query(name, qtype):
    ident = random.randint(0, 65535)

    packet = bytearray()

    # Header
    packet += ident.to_bytes(2, "big")
    packet += b"\x01\x00"       # recursion desired
    packet += b"\x00\x01"       # one question
    packet += b"\x00\x00"       # answers
    packet += b"\x00\x00"       # authority
    packet += b"\x00\x00"       # additional

    # Question
    packet += _encode_name(name)
    packet += qtype.to_bytes(2, "big")
    packet += b"\x00\x01"       # IN

    s = net.udp_connect(DNS_SERVER, 53)

    try:
        s.send(packet)

        data = s.recv(512)

    finally:
        net.safe_close(s)

    return data


def _parse_answers(data):
    qdcount = int.from_bytes(data[4:6], "big")
    ancount = int.from_bytes(data[6:8], "big")

    offset = 12

    # Skip questions
    for _ in range(qdcount):
        _, offset = _decode_name(data, offset)
        offset += 4

    answers = []

    for _ in range(ancount):
        _, offset = _decode_name(data, offset)

        rtype = int.from_bytes(data[offset:offset + 2], "big")
        offset += 2

        offset += 2       # class
        offset += 4       # ttl

        length = int.from_bytes(data[offset:offset + 2], "big")
        offset += 2

        rdata = data[offset:offset + length]
        offset += length

        answers.append((rtype, rdata))

    return answers


def _is_ipv4(value):
    parts = value.split(".")

    if len(parts) != 4:
        return False

    for p in parts:
        try:
            n = int(p)

            if n < 0 or n > 255:
                return False

        except Exception:
            return False

    return True


def _forward(host):
    data = _dns_query(host, 1)   # A record

    answers = _parse_answers(data)

    print("Name: {}".format(host))

    found = False

    for rtype, rdata in answers:
        if rtype == 1 and len(rdata) == 4:
            found = True
            print("  Family:  IPv4")
            print(
                "  Address: {}.{}.{}.{}".format(
                    rdata[0],
                    rdata[1],
                    rdata[2],
                    rdata[3],
                )
            )

    if not found:
        print("  No IPv4 addresses found")


def _reverse(addr):
    query = ".".join(reversed(addr.split(".")))
    query += ".in-addr.arpa"

    data = _dns_query(query, 12)   # PTR

    answers = _parse_answers(data)

    print("Address: {}".format(addr))

    found = False

    for rtype, rdata in answers:
        if rtype == 12:
            name, _ = _decode_name(data, data.index(rdata))
            print("  Name: {}".format(name))
            found = True

    if not found:
        print("  No PTR record found")


def main(host):
    try:
        if _is_ipv4(host):
            _reverse(host)
        else:
            _forward(host)

    except Exception as e:
        print("nslookup: {}: {}".format(host, e))
