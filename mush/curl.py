__doc__ = """
NAME
    curl - simple HTTP client

SYNOPSIS
    curl(url, method="GET", data=None, timeout=5000,
         headers=None, redirects=5,
         show_headers=False, collect=False)

DESCRIPTION
    Sends HTTP requests and streams responses.

    Supports:
        - GET, POST, HEAD, and arbitrary methods
        - custom headers
        - redirects
        - streamed output

OPTIONS
    method:
        HTTP request method.

    data:
        Request body for POST and other methods.

    headers:
        Additional HTTP headers.

    timeout:
        Connection timeout in milliseconds.

    redirects:
        Maximum redirect count.

    show_headers:
        Display response headers.

    collect:
        Return response data instead of printing.

RETURNS
    collect=False:
        None on success.

    collect=True:
        Dictionary containing:
            status
            headers
            body

    False on failure.

EXAMPLES
    curl(
        "https://example.com"
    )

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

    curl(
        "https://example.com",
        collect=True,
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


def _read_body(response):
    data = b""

    for chunk in response.body_iter():
        data += chunk

    return data


def _print_body(data):
    try:
        print(
            data.decode(
                "utf-8",
                "ignore",
            ),
            end="",
        )

    except Exception:
        print(data)


def main(
    url,
    method="GET",
    data=None,
    timeout=5000,
    headers=None,
    redirects=5,
    show_headers=False,
    collect=False,
):
    if not url:
        print(
            "curl: missing URL"
        )
        return False

    if headers is None:
        headers = {}

    else:
        headers = dict(headers)

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

        body = _read_body(
            response
        )

        if collect:
            return {
                "status": response.status,
                "headers": dict(
                    response.headers
                ),
                "body": body,
            }

        if show_headers:
            print(
                response.status
            )

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

        _print_body(body)

        return None

    except Exception as e:
        print(
            "curl: {}".format(e)
        )

        return False

    finally:
        if response:
            try:
                response.close()
            except Exception:
                pass
