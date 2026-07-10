__doc__ = """
NAME
    curl - simple HTTP client

SYNOPSIS
    curl(
        url,
        method="GET",
        data=None,
        timeout=5000,
        headers=None,
        redirects=5,
        show_headers=False,
    )

DESCRIPTION
    Sends HTTP requests and streams responses.

    Supports:
        - GET, POST, HEAD, and arbitrary methods
        - custom headers
        - redirects
        - streamed output

EXAMPLES
    curl("https://example.com")

    curl(
        "https://postman-echo.com/post",
        method="POST",
        data="hello=mush",
    )

    curl(
        "https://example.com",
        method="HEAD",
        show_headers=True,
    )
"""
import mush
http = mush._load_internal("_http")
net = mush._load_internal("_net")
def _connect(info, timeout):
    sock = net["tcp_connect"](
        info["host"],
        info["port"],
        timeout,
    )
    if info["tls"]:
        sock = net["tls_wrap"](
            sock,
            info["host"],
        )
    return sock
def _print_body(response):
    for chunk in response.body_iter():
        try:
            print(
                chunk.decode(
                    "utf-8",
                    "ignore",
                ),
                end="",
            )
        except Exception:
            print(chunk)
def main(
    url,
    method="GET",
    data=None,
    timeout=5000,
    headers=None,
    redirects=5,
    show_headers=False,
):
    if headers is None:
        headers = {}
    if "Accept-Encoding" not in headers:
        headers["Accept-Encoding"] = (
            "identity"
        )
    response = None
    try:
        response = http["request"](
            url,
            method=method,
            body=data,
            headers=headers,
            timeout=timeout,
            redirects=redirects,
            connect=_connect,
        )
        if show_headers:
            print(response.status)
            for key, value in (
                response.headers.items()
            ):
                print(
                    "{}: {}".format(
                        key,
                        value,
                    )
                )
            print()
        _print_body(response)
    except Exception as e:
        print(
            "curl:",
            e,
        )
    finally:
        if response:
            response.close()
