__doc__ = """
NAME
    ipcalc - calculate IPv4 network information

SYNOPSIS
    ipcalc(address, netmask=None)

DESCRIPTION
    Calculates IPv4 network, broadcast, and host information.

EXAMPLES
    ipcalc("192.168.1.50/24")

    ipcalc(
        "192.168.1.50",
        netmask="255.255.255.0",
    )
"""
def _parse_ip(ip):
    parts = ip.split(".")
    if len(parts) != 4:
        raise ValueError("invalid IPv4 address")
    return tuple(int(x) for x in parts)
def _format_ip(ip):
    return ".".join(str(x) for x in ip)
def _mask_from_prefix(bits):
    if bits == 0:
        return 0
    return (0xffffffff << (32 - bits)) & 0xffffffff
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
    while mask:
        bits += mask & 1
        mask >>= 1
    return bits
def main(address, netmask=None):
    if "/" in address:
        addr, prefix = address.split("/", 1)
        bits = int(prefix)
    else:
        addr = address
        bits = None
    ip = _parse_ip(addr)
    if netmask:
        mask = _ip_int(_parse_ip(netmask))
    elif bits is not None:
        mask = _mask_from_prefix(bits)
    else:
        raise ValueError("missing netmask")
    ip_num = _ip_int(ip)
    network = ip_num & mask
    broadcast = network | (~mask & 0xffffffff)
    print("Address:     {}".format(_format_ip(ip)))
    print(
        "Netmask:     {}".format(
            _format_ip(_int_ip(mask))
        )
    )
    print(
        "CIDR:        /{}".format(
            _prefix(mask)
        )
    )
    print(
        "Network:     {}".format(
            _format_ip(_int_ip(network))
        )
    )
    print(
        "Broadcast:   {}".format(
            _format_ip(_int_ip(broadcast))
        )
    )
