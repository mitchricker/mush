__doc__ = """
NAME
    wget - download files over HTTP

SYNOPSIS
    wget(
        url,
        out=None,
        timeout=5000,
        headers=None,
        redirects=5,
        recursive=False,
        depth=1,
        max_files=16,
        progress=True,
    )

DESCRIPTION
    Downloads files using HTTP GET.

    Supports:
        - redirects
        - streamed writes
        - atomic output
        - shallow recursive HTML downloads

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

EXAMPLES
    wget(
        "https://example.com/file.bin"
    )

    wget(
        "https://example.com/",
        recursive=True,
        depth=1,
    )
"""
__doc__ = """
NAME
    wget - download files over HTTP

SYNOPSIS
    wget(url, out=None, timeout=5000, headers=None,
         redirects=5, recursive=False, depth=1,
         max_files=16, progress=True)

DESCRIPTION
    Downloads files using HTTP GET.

    Supports:
        - redirects
        - streamed writes
        - atomic output
        - recursive HTML downloads
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
    if link.startswith((
        "#",
        "mailto:",
        "javascript:",
        "data:",
    )):
        return False
    return True
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
        if not data:
            return
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
            link = match.group(1)
            self.links.append(link)
            consumed = match.group(0)
            self.buf = self.buf[
                len(consumed):
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
        headers=headers,
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
    return scanner
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
    name = _filename(url)
    try:
        print(
            "{} -> {}".format(
                url,
                name,
            )
        )
        scanner = _download(
            url,
            name,
            timeout,
            headers,
            redirects,
            progress,
        )
        state["count"] += 1
    except Exception as e:
        print(
            "wget: {}: {}".format(
                url,
                e,
            )
        )
        return
    if (
        scanner
        and depth < max_depth
    ):
        for link in scanner.links:
            if not _valid_link(link):
                continue
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
):
    if recursive:
        _recursive(
            url,
            0,
            depth,
            {
                "seen": [],
                "count": 0,
                "max_files": max_files,
            },
            timeout,
            headers,
            redirects,
            progress,
        )
        return
    if out is None:
        out = _filename(url)
    try:
        _download(
            url,
            out,
            timeout,
            headers,
            redirects,
            progress,
        )
        print(out)
    except Exception as e:
        print("wget: ", e,)
