__doc__ = """
NAME
    ipcalc - calculate IPv4 network information

SYNOPSIS
    ipcalc(address, netmask=None, collect=False)

DESCRIPTION
    Calculates IPv4 network, broadcast, and host information.

    Returns:
        collect=False:
            None on success.

        collect=True:
            Tuple containing:
            (
                address,
                netmask,
                cidr,
                network,
                broadcast
            )

        False on failure.

EXAMPLES
    ipcalc(
        "192.168.1.50/24"
    )

    ipcalc(
        "192.168.1.50",
        netmask="255.255.255.0",
    )

    ipcalc(
        "192.168.1.50/24",
        collect=True,
    )
"""


def _parse_ip(ip):
    ip = ip.strip()

    parts = ip.split(".")

    if len(parts) != 4:
        raise ValueError(
            "invalid IPv4 address"
        )

    result = []

    for part in parts:
        if not part:
            raise ValueError(
                "invalid IPv4 address"
            )

        value = int(part)

        if value < 0 or value > 255:
            raise ValueError(
                "invalid IPv4 address"
            )

        result.append(value)

    return tuple(result)


def _format_ip(ip):
    return ".".join(
        str(x)
        for x in ip
    )


def _mask_from_prefix(bits):
    if bits < 0 or bits > 32:
        raise ValueError(
            "invalid CIDR prefix"
        )

    if bits == 0:
        return 0

    return (
        0xffffffff << (32 - bits)
    ) & 0xffffffff


def _ip_int(ip):
    a, b, c, d = ip

    return (
        (a << 24)
        | (b << 16)
        | (c << 8)
        | d
    )


def _int_ip(value):
    return (
        (value >> 24) & 255,
        (value >> 16) & 255,
        (value >> 8) & 255,
        value & 255,
    )


def _prefix(mask):
    bits = 0
    seen_zero = False

    for i in range(32):
        bit = (
            mask >> (31 - i)
        ) & 1

        if bit:
            if seen_zero:
                raise ValueError(
                    "invalid netmask"
                )

            bits += 1

        else:
            seen_zero = True

    return bits


def _parse_prefix(value):
    bits = int(value)

    if bits < 0 or bits > 32:
        raise ValueError(
            "invalid CIDR prefix"
        )

    return bits


def main(
    address,
    netmask=None,
    collect=False,
):
    try:
        if not isinstance(address, str):
            raise ValueError(
                "invalid IPv4 address"
            )

        address = address.strip()

        bits = None

        if "/" in address:
            addr, prefix = address.split(
                "/",
                1,
            )

            bits = _parse_prefix(
                prefix
            )

        else:
            addr = address

        ip = _parse_ip(addr)

        if netmask is not None:
            mask = _ip_int(
                _parse_ip(netmask)
            )

            cidr = _prefix(mask)

        elif bits is not None:
            mask = _mask_from_prefix(
                bits
            )

            cidr = bits

        else:
            raise ValueError(
                "missing netmask"
            )

        ip_num = _ip_int(ip)

        network = ip_num & mask

        broadcast = (
            network
            | (~mask & 0xffffffff)
        )

        result = (
            _format_ip(ip),
            _format_ip(_int_ip(mask)),
            cidr,
            _format_ip(_int_ip(network)),
            _format_ip(_int_ip(broadcast)),
        )

    except Exception as e:
        print(
            "ipcalc: {}".format(e)
        )

        return False

    if collect:
        return result

    print(
        "Address:     {}".format(
            result[0]
        )
    )

    print(
        "Netmask:     {}".format(
            result[1]
        )
    )

    print(
        "CIDR:        /{}".format(
            result[2]
        )
    )

    print(
        "Network:     {}".format(
            result[3]
        )
    )

    print(
        "Broadcast:   {}".format(
            result[4]
        )
    )

    return None
