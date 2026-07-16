"""
Internal network helpers.

Provides:
    resolve()
    tcp_connect()
    udp_connect()
    tls_wrap()
    recv_iter()
    safe_close()

Used by networking services and protocol helpers.

Functions:

    resolve(host, port)

        Resolve a hostname.

        Returns:
            Socket address tuple.


    tcp_connect(host, port, timeout=2000)

        Open a TCP connection.

        Returns:
            Connected socket.


    udp_connect(host, port, timeout=2000)

        Open a UDP connection.

        Returns:
            Connected socket.


    tls_wrap(sock, host=None)

        Wrap a socket with TLS.

        Uses:
            ssl when available.
            ussl as a fallback.

        Returns:
            TLS socket.


    recv_iter(sock, timeout=2000, chunk=256)

        Yield received data chunks.


    safe_close(sock)

        Close a socket safely.

Designed for MicroPython compatibility across:
    - ESP32 builds using ssl
    - older builds using ussl
    - normal sockets
    - TLS sockets
"""
import socket
import time


def resolve(host, port):
    return socket.getaddrinfo(
        host,
        port,
    )[0][-1]


def _connect(
    host,
    port,
    sock_type,
    timeout=2000,
):
    addr = resolve(
        host,
        port,
    )

    sock = socket.socket(
        socket.AF_INET,
        sock_type,
    )

    try:
        try:
            sock.settimeout(
                timeout / 1000
            )
        except Exception:
            pass

        sock.connect(addr)

        return sock

    except Exception:
        try:
            sock.close()
        except Exception:
            pass

        raise


def tcp_connect(
    host,
    port,
    timeout=2000,
):
    return _connect(
        host,
        port,
        socket.SOCK_STREAM,
        timeout,
    )


def udp_connect(
    host,
    port,
    timeout=2000,
):
    return _connect(
        host,
        port,
        socket.SOCK_DGRAM,
        timeout,
    )


def tls_wrap(
    sock,
    host=None,
):

    import gc

    gc.collect()

    errors = []

    try:
        import ssl

        if (
            hasattr(ssl, "SSLContext")
            and hasattr(
                ssl,
                "PROTOCOL_TLS_CLIENT",
            )
        ):
            try:
                ctx = ssl.SSLContext(
                    ssl.PROTOCOL_TLS_CLIENT
                )

                if hasattr(
                    ctx,
                    "check_hostname",
                ):
                    ctx.check_hostname = False

                if hasattr(
                    ctx,
                    "verify_mode",
                ):
                    ctx.verify_mode = (
                        ssl.CERT_NONE
                    )

                return ctx.wrap_socket(
                    sock,
                    server_hostname=host,
                )

            except Exception as e:
                errors.append(
                    "SSLContext: {}".format(e)
                )

        try:
            return ssl.wrap_socket(
                sock,
                server_hostname=host,
            )

        except Exception as e:
            errors.append(
                "ssl.wrap_socket: {}".format(e)
            )

    except Exception as e:
        errors.append(
            "ssl import: {}".format(e)
        )

    try:
        import ussl

        try:
            return ussl.wrap_socket(
                sock,
                server_hostname=host,
            )

        except Exception as e:
            errors.append(
                "ussl: {}".format(e)
            )

    except Exception as e:
        errors.append(
            "ussl import: {}".format(e)
        )

    try:
        sock.close()
    except Exception:
        pass

    raise OSError(
        "TLS failed: "
        +
        "; ".join(errors)
    )


def send(sock, data):

    if hasattr(
        sock,
        "send",
    ):
        return sock.send(data)

    return sock.write(data)


def recv(
    sock,
    size=256,
):

    if hasattr(
        sock,
        "recv",
    ):
        return sock.recv(size)

    return sock.read(size)


def recv_iter(
    sock,
    timeout=2000,
    chunk=256,
):

    start = time.ticks_ms()

    while True:
        try:
            data = recv(
                sock,
                chunk,
            )

            if not data:
                break

            yield data

        except Exception:
            break

        if (
            timeout
            and time.ticks_diff(
                time.ticks_ms(),
                start,
            ) > timeout
        ):
            break


def safe_close(sock):
    if sock:
        try:
            sock.close()
        except Exception:
            pass
