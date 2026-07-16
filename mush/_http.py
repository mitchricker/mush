"""
Internal HTTP helper.

Provides:
    request()
    request_once()
    parse_url()
    join_url()

Supports:
    - HTTP and HTTPS connections
    - redirects
    - JSON responses
    - streaming response bodies

Functions:

    parse_url(url)

        Parse a URL.

        Returns:
            {
                host,
                path,
                port,
                tls
            }


    request(url, ...)

        Perform an HTTP request.

        Supports redirects.

        Returns:
            Response object


    request_once(url, ...)

        Perform a single HTTP request.

        Returns:
            Response object


    join_url(base, location)

        Resolve redirect URLs.


Response:

    code()

        Return HTTP status code.


    body_iter()

        Yield response body chunks.


    json()

        Decode JSON response body.


    close()

        Close the underlying socket.

Designed for MicroPython memory constraints.
"""
_CHUNK = 256

_REDIRECTS = (
    301,
    302,
    303,
    307,
    308,
)


def parse_url(url):
    tls = False

    if url.startswith("https://"):
        tls = True
        url = url[8:]

    elif url.startswith("http://"):
        url = url[7:]

    else:
        raise ValueError(
            "unsupported URL scheme"
        )

    if "/" in url:
        host, path = url.split("/", 1)
        path = "/" + path
    else:
        host = url
        path = "/"

    port = 443 if tls else 80

    if ":" in host:
        host, port_text = host.rsplit(":", 1)
        port = int(port_text)

    return {
        "host": host,
        "path": path,
        "port": port,
        "tls": tls,
    }


def host_header(info):
    if (
        info["tls"]
        and info["port"] == 443
    ):
        return info["host"]

    if (
        not info["tls"]
        and info["port"] == 80
    ):
        return info["host"]

    return "{}:{}".format(
        info["host"],
        info["port"],
    )


def join_url(base, location):
    if location.startswith(
        (
            "http://",
            "https://",
        )
    ):
        return location

    info = parse_url(base)

    scheme = (
        "https"
        if info["tls"]
        else "http"
    )

    if location.startswith("/"):
        path = location

    else:
        base_path = info["path"].rsplit(
            "/",
            1,
        )[0]

        path = (
            base_path
            + "/"
            + location
        )

    if (
        (info["tls"] and info["port"] == 443)
        or (
            not info["tls"]
            and info["port"] == 80
        )
    ):
        return "{}://{}{}".format(
            scheme,
            info["host"],
            path,
        )

    return "{}://{}:{}{}".format(
        scheme,
        info["host"],
        info["port"],
        path,
    )


def open(sock, method, info, headers=None, body=None):
    lines = [
        "{} {} HTTP/1.1".format(
            method.upper(),
            info["path"],
        ),
        "Host: {}".format(
            host_header(info),
        ),
        "Connection: close",
        "Accept-Encoding: identity",
    ]

    if headers:
        for key, value in headers.items():
            lines.append(
                "{}: {}".format(
                    key,
                    value,
                )
            )

    if body:
        if isinstance(body, str):
            body = body.encode()

        lines.append(
            "Content-Length: {}".format(
                len(body),
            )
        )

    lines.extend(
        (
            "",
            "",
        )
    )

    sock.send(
        "\r\n".join(lines).encode()
    )

    if body:
        sock.send(body)

    return Response(sock)


def request_once(
    url,
    method="GET",
    headers=None,
    body=None,
    timeout=5000,
    connect=None,
):
    if connect is None:
        raise ValueError(
            "missing connect function"
        )

    info = parse_url(url)

    sock = connect(
        info,
        timeout,
    )

    return open(
        sock,
        method,
        info,
        headers,
        body,
    )


def request(
    url,
    method="GET",
    headers=None,
    body=None,
    timeout=5000,
    redirects=5,
    connect=None,
):
    while True:
        response = request_once(
            url,
            method,
            headers,
            body,
            timeout,
            connect,
        )

        code = response.code()

        if code not in _REDIRECTS:
            return response

        if redirects <= 0:
            response.close()
            raise OSError(
                "too many redirects"
            )

        location = response.headers.get(
            "location"
        )

        if not location:
            return response

        response.close()

        url = join_url(
            url,
            location,
        )

        redirects -= 1


class Response:

    def __init__(self, sock):
        self.sock = sock
        self.status = ""
        self.headers = {}
        self._initial = b""

        self._read_headers()


    def _read_headers(self):
        data = b""

        while b"\r\n\r\n" not in data:
            chunk = self.sock.recv(_CHUNK)

            if not chunk:
                break

            data += chunk

        if b"\r\n\r\n" not in data:
            raise OSError(
                "invalid HTTP response"
            )

        header, self._initial = data.split(
            b"\r\n\r\n",
            1,
        )

        lines = header.decode(
            "utf-8",
            "ignore",
        ).split("\r\n")

        self.status = lines[0]

        for line in lines[1:]:

            if ":" in line:
                key, value = line.split(
                    ":",
                    1,
                )

                self.headers[
                    key.lower()
                ] = value.strip()


    def code(self):
        try:
            return int(
                self.status.split()[1]
            )

        except Exception:
            return 0


    def body_iter(self):

        if (
            self.headers.get(
                "transfer-encoding",
                "",
            ).lower()
            == "chunked"
        ):
            yield from self._chunked()
            return


        if self._initial:
            yield self._initial
            self._initial = b""


        if "content-length" in self.headers:

            remaining = int(
                self.headers[
                    "content-length"
                ]
            )

            while remaining:

                data = self.sock.recv(
                    min(
                        _CHUNK,
                        remaining,
                    )
                )

                if not data:
                    break

                remaining -= len(data)

                yield data

            return


        while True:

            data = self.sock.recv(
                _CHUNK
            )

            if not data:
                break

            yield data


    def _readline(self):

        line = b""

        while True:

            if b"\r\n" in self._initial:

                part, self._initial = (
                    self._initial.split(
                        b"\r\n",
                        1,
                    )
                )

                return (
                    line
                    + part
                    + b"\r\n"
                )

            if self._initial:

                line += self._initial
                self._initial = b""

            data = self.sock.recv(1)

            if not data:
                return line

            line += data


    def _chunked(self):

        while True:

            line = self._readline()

            if not line:
                return

            size = int(
                line.strip(),
                16,
            )

            if size == 0:
                return

            remaining = size

            while remaining:

                if self._initial:

                    data = self._initial[
                        :min(
                            _CHUNK,
                            remaining,
                        )
                    ]

                    self._initial = (
                        self._initial[
                            len(data):
                        ]
                    )

                else:

                    data = self.sock.recv(
                        min(
                            _CHUNK,
                            remaining,
                        )
                    )

                if not data:
                    return

                remaining -= len(data)

                yield data


            if self._initial.startswith(
                b"\r\n"
            ):
                self._initial = (
                    self._initial[2:]
                )

            else:
                self.sock.recv(2)


    def json(self):
        import json

        data = b""

        for chunk in self.body_iter():
            data += chunk

        return json.loads(
            data.decode(
                "utf-8",
                "ignore",
            )
        )


    def close(self):
        try:
            self.sock.close()

        except Exception:
            pass
