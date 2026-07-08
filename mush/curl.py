__doc__ = """
NAME
    curl - simple HTTP/HTTPS client

SYNOPSIS
    curl(url)
    curl(url, method="GET", data=None, timeout=2000)

DESCRIPTION
    Minimal HTTP/HTTPS client for MicroPython.

    Supports basic HTTP methods over TCP.

    HTTPS uses TLS via ussl (preferred) or ssl (fallback).

EXAMPLES
    curl("http://example.com")
    curl("https://example.com")
    curl("https://example.com/api", method="POST", data="x=1")
    curl("https://example.com", method="HEAD")
"""

import mush._net as net


def _parse_url(url):
    if url.startswith("https://"):
        return "https", url[8:]

    if url.startswith("http://"):
        return "http", url[7:]

    raise ValueError("only http:// and https:// supported")


def _parse_host_path(rest):
    parts = rest.split("/", 1)

    host = parts[0]
    path = "/" + parts[1] if len(parts) > 1 else "/"

    port = None

    if ":" in host:
        host, port_text = host.rsplit(":", 1)
        port = int(port_text)

    return host, path, port


def main(url, method="GET", data=None, timeout=2000):
    sock = None

    try:
        scheme, rest = _parse_url(url)
        host, path, port = _parse_host_path(rest)

        if port is None:
            port = 443 if scheme == "https" else 80

        sock = net.tcp_connect(host, port, timeout)

        if scheme == "https":
            sock = net.tls_wrap(sock, host)

        method = method.upper()

        if data is not None and isinstance(data, str):
            data = data.encode()

        request = "{} {} HTTP/1.0\r\n".format(method, path)
        request += "Host: {}\r\n".format(host)
        request += "User-Agent: mush-curl\r\n"

        if data is not None:
            request += "Content-Length: {}\r\n".format(len(data))

        request += "\r\n"

        sock.send(request.encode())

        if data is not None:
            sock.send(data)

        while True:
            chunk = sock.recv(256)

            if not chunk:
                break

            try:
                print(chunk.decode("utf-8"), end="")
            except Exception:
                print(chunk)

    except Exception as e:
        print("curl:", e)

    finally:
        if sock:
            net.safe_close(sock)
