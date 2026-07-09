__doc__ = """
NAME
    nc - simple TCP client/server (netcat-style)

SYNOPSIS
    nc(host, port, data=..., timeout=2000)
    nc(host, port, listen=True, timeout=0, raw=False)

DESCRIPTION
    Minimal netcat-like tool for MicroPython.

    Supports:
      - TCP client mode
      - single-process multiplexed listener
      - raw byte streaming

EXAMPLES
    nc("example.com", 80, data="GET / HTTP/1.0\r\n\r\n")

    nc("0.0.0.0", 1234, listen=True)

    nc("0.0.0.0", 1234, listen=True, raw=True)
"""
import sys
import mush
net = mush._load_internal("_net")
def _write(buf, raw):
    if raw:
        try:
            sys.stdout.buffer.write(buf)
        except Exception:
            print(buf)
    else:
        try:
            print(buf.decode(errors="ignore"), end="")
        except Exception:
            print(buf, end="")
def _client(host, port, data, timeout, raw):
    s = None
    try:
        s = net["tcp_connect"](host, port, timeout)
        if data:
            if isinstance(data, str):
                data = data.encode()
            s.send(data)
        for chunk in net["recv_iter"](s, timeout):
            _write(chunk, raw)
    finally:
        if s:
            net["safe_close"](s)
def _serve(conn, addr, timeout, raw):
    print("nc:", addr)
    for chunk in net["recv_iter"](conn, timeout):
        _write(chunk, raw)
def _server(host, port, timeout, raw):
    import socket
    addr = net["resolve"](host, port)
    s = None
    try:
        s = socket.socket()
        s.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1,
        )
        s.bind(addr)
        s.listen(1)
        print(
            "nc: listening on {}:{}".format(
                host,
                port,
            )
        )
        while True:
            conn, client = s.accept()
            try:
                _serve(conn, client, timeout, raw)
            finally:
                net["safe_close"](conn)
    finally:
        if s:
            net["safe_close"](s)
def main(host, port, data=None, listen=False, timeout=2000, raw=False):
    try:
        if listen:
            _server(host, port, timeout, raw)
        else:
            _client(host, port, data, timeout, raw)
    except KeyboardInterrupt:
        print("\nnc: interrupted")
    except Exception as e:
        print("nc:", e)
