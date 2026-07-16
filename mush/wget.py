__doc__ = """
NAME
    wget - download files over HTTP

SYNOPSIS
    wget(url, out=None, timeout=5000, headers=None, redirects=5,
         recursive=False, depth=1, max_files=16,
         progress=True, collect=False)

DESCRIPTION
    Downloads files using HTTP GET.

    Supports:
        - HTTPS
        - redirects
        - streamed writes
        - atomic output
        - recursive HTML downloads

OPTIONS
    out:
        Output filename.

    timeout:
        Connection timeout in milliseconds.

    headers:
        Additional HTTP headers.

    redirects:
        Maximum redirect count.

    recursive:
        Download linked resources.

    depth:
        Maximum recursion depth.

    max_files:
        Maximum number of files.

    progress:
        Display download progress.

    collect:
        Return download information.

RETURNS
    collect=True:
        Dictionary containing:
            url
            output
            bytes
            links

        Recursive:
            list of download dictionaries

    collect=False:
        None on success

    False on failure.

EXAMPLES
    wget(
        "https://example.com/file.bin"
    )

    wget(
        "https://example.com/",
        recursive=True,
        depth=1,
    )

    wget(
        "https://example.com/file.bin",
        collect=True,
    )
"""

import re
import mush

http = mush._load_internal("_http")
net = mush._load_internal("_net")
fsio = mush._load_internal("_fsio")


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


def _filename(url):
    url = url.split("?", 1)[0]
    url = url.split("#", 1)[0]
    url = url.rstrip("/")

    if "/" in url:
        name = url.rsplit("/", 1)[1]

        if name:
            return name

    return "index.html"


def _valid_link(link):
    if not link:
        return False

    return not link.startswith(
        (
            "#",
            "mailto:",
            "javascript:",
            "data:",
        )
    )


def _join(base, link):
    return http["join_url"](
        base,
        link,
    )


class LinkScanner:

    def __init__(self):
        self.buf = ""
        self.links = []

    def feed(self, data):
        try:
            self.buf += data.decode(
                "utf-8",
                "ignore",
            )

        except Exception:
            return

        while True:
            match = re.search(
                'href=["\']([^"\']+)["\']',
                self.buf,
            )

            if not match:
                break

            self.links.append(
                match.group(1)
            )

            self.buf = self.buf[
                len(match.group(0)):
            ]

        if len(self.buf) > 256:
            self.buf = self.buf[-128:]


def _is_html(response, name):
    content = response.headers.get(
        "content-type",
        "",
    ).lower()

    if "text/html" in content:
        return True

    name = name.lower()

    return (
        name.endswith(".html")
        or name.endswith(".htm")
    )


def _download(
    url,
    out,
    timeout,
    headers,
    redirects,
    progress,
):
    response = http["request"](
        url,
        method="GET",
        headers=headers or {},
        timeout=timeout,
        redirects=redirects,
        connect=_connect,
    )

    scanner = None

    if _is_html(response, out):
        scanner = LinkScanner()

    count = 0

    try:
        def writer(f):
            nonlocal count

            for chunk in response.body_iter():
                f.write(chunk)

                count += len(chunk)

                if scanner:
                    scanner.feed(chunk)

                if progress:
                    print(
                        "\r{} bytes".format(
                            count
                        ),
                        end="",
                    )

            if progress:
                print()

        fsio["atomic_write"](
            out,
            writer,
        )

    finally:
        response.close()

    return (
        count,
        scanner,
    )


def _recursive(
    url,
    depth,
    max_depth,
    state,
    timeout,
    headers,
    redirects,
    progress,
):
    if depth > max_depth:
        return

    if state["count"] >= state["max_files"]:
        return

    if url in state["seen"]:
        return

    if not _valid_link(url):
        return

    state["seen"].append(url)

    out = _filename(url)

    try:
        print(
            "{} -> {}".format(
                url,
                out,
            )
        )

        count, scanner = _download(
            url,
            out,
            timeout,
            headers,
            redirects,
            progress,
        )

        item = {
            "url": url,
            "output": out,
            "bytes": count,
        }

        state["files"].append(item)
        state["count"] += 1

    except Exception as e:
        print(
            "wget: {}: {}".format(
                url,
                e,
            )
        )
        return

    if scanner and depth < max_depth:
        for link in scanner.links:
            _recursive(
                _join(url, link),
                depth + 1,
                max_depth,
                state,
                timeout,
                headers,
                redirects,
                progress,
            )


def main(
    url,
    out=None,
    timeout=5000,
    headers=None,
    redirects=5,
    recursive=False,
    depth=1,
    max_files=16,
    progress=True,
    collect=False,
):
    try:
        if recursive:
            state = {
                "seen": [],
                "files": [],
                "count": 0,
                "max_files": max_files,
            }

            _recursive(
                url,
                0,
                depth,
                state,
                timeout,
                headers,
                redirects,
                progress,
            )

            if collect:
                return state["files"]

            return None


        if out is None:
            out = _filename(url)

        count, scanner = _download(
            url,
            out,
            timeout,
            headers,
            redirects,
            progress,
        )

        if collect:
            return {
                "url": url,
                "output": out,
                "bytes": count,
                "links": (
                    scanner.links
                    if scanner
                    else []
                ),
            }

        print(
            "saved: {}".format(
                out
            )
        )

        return None

    except Exception as e:
        print(
            "wget: {}".format(
                e
            )
        )

        return False
