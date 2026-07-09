import socket
import time
def resolve(host, port):
    return socket.getaddrinfo(host, port)[0][-1]
def _connect(host, port, sock_type, timeout=2000):
    addr = resolve(host, port)
    s = socket.socket(socket.AF_INET, sock_type)
    try:
        try:
            s.settimeout(timeout / 1000)
        except Exception:
            pass
        s.connect(addr)
        return s
    except Exception:
        try:
            s.close()
        except Exception:
            pass
        raise
def tcp_connect(host, port, timeout=2000):
    return _connect(host, port, socket.SOCK_STREAM, timeout)
def udp_connect(host, port, timeout=2000):
    return _connect(host, port, socket.SOCK_DGRAM, timeout)
def tls_wrap(sock, host=None):
    try:
        import ssl
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        return ctx.wrap_socket(sock, server_hostname=host,)
    except Exception:
        try:
            import ussl
            if host:
                return ussl.wrap_socket(sock, server_hostname=host,)
            return ussl.wrap_socket(sock)
        except Exception:
            try:
                sock.close()
            except Exception:
                pass
            raise OSError("TLS not supported on this firmware")
def recv_iter(sock, timeout=2000, chunk=256):
    start = time.ticks_ms()
    while True:
        try:
            data = sock.recv(chunk)
            if not data:
                break
            yield data
        except Exception:
            break
        if timeout and time.ticks_diff(time.ticks_ms(), start) > timeout:
            break
def safe_close(sock):
    try:
        sock.close()
    except Exception:
        pass
