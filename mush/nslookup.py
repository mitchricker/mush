__doc__ = """
NAME
    nslookup - query DNS for a hostname or address

SYNOPSIS
    nslookup(host,[server="8.8.8.8"])

DESCRIPTION
    Performs DNS lookups.

EXAMPLES
    nslookup("example.com")
    nslookup("8.8.8.8")
    nslookup("example.com",server="1.1.1.1")
"""
import random
import mush
net = mush._load_internal("_net")
def _encode_name(name):
    out = b""
    for part in name.split("."):
        out += bytes([len(part)]) + part.encode()
    return out + b"\x00"
def _decode_name(data,offset):
    labels = []
    while True:
        if offset >= len(data):
            raise OSError("short DNS name")
        length = data[offset]
        if length == 0:
            return ".".join(labels),offset + 1
        if length & 0xc0:
            ptr = ((length & 0x3f) << 8) | data[offset + 1]
            label,_ = _decode_name(data,ptr)
            labels.append(label)
            return ".".join(labels),offset + 2
        offset += 1
        if offset + length > len(data):
            raise OSError("short DNS label")
        labels.append(data[offset:offset + length].decode("utf-8","ignore"))
        offset += length
def _dns_query(server,name,qtype):
    ident = random.randint(0,65535)
    packet = bytearray(
        ident.to_bytes(2,"big") +
        b"\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00"
    )
    packet += _encode_name(name)
    packet += qtype.to_bytes(2,"big") + b"\x00\x01"
    s = net["udp_connect"](server,53)
    try:
        s.send(packet)
        return s.recv(512)
    finally:
        net["safe_close"](s)
def _parse_answers(data):
    answers = []
    offset = 12
    qd = int.from_bytes(data[4:6],"big")
    an = int.from_bytes(data[6:8],"big")
    for _ in range(qd):
        _,offset = _decode_name(data,offset)
        offset += 4
    for _ in range(an):
        _,offset = _decode_name(data,offset)
        rtype = int.from_bytes(data[offset:offset + 2],"big")
        offset += 8
        length = int.from_bytes(data[offset:offset + 2],"big")
        offset += 2
        answers.append((rtype,data[offset:offset + length],offset))
        offset += length
    return answers
def _is_ipv4(value):
    parts = value.split(".")
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(p) <= 255 for p in parts)
    except:
        return False
def _forward(server,host):
    print("Name: {}".format(host))
    found = False
    for rtype,rdata,_ in _parse_answers(_dns_query(server,host,1)):
        if rtype == 1 and len(rdata) == 4:
            print("  Family:  IPv4")
            print("  Address: {}.{}.{}.{}".format(*rdata))
            found = True
    if not found:
        print("  No IPv4 addresses found")
def _reverse(server,addr):
    query = ".".join(reversed(addr.split("."))) + ".in-addr.arpa"
    data = _dns_query(server,query,12)
    print("Address: {}".format(addr))
    found = False
    for rtype,_,offset in _parse_answers(data):
        if rtype == 12:
            name,_ = _decode_name(data,offset)
            print("  Name: {}".format(name))
            found = True
    if not found:
        print("  No PTR record found")
def main(host,server="8.8.8.8"):
    try:
        if _is_ipv4(host):
            _reverse(server,host)
        else:
            _forward(server,host)
    except Exception as e:
        print("nslookup: {}: {}".format(host,e))
