__doc__ = """
NAME
    whois - query registration information

SYNOPSIS
    whois(query, verbose=False, collect=False)

DESCRIPTION
    Performs a WHOIS-style lookup using RDAP.

    Returns:
        collect=False:
            None on success
            False on failure

        collect=True:
            Parsed RDAP response dictionary

EXAMPLES
    whois("example.com")

    whois("8.8.8.8")

    whois(
        "example.com",
        verbose=True,
    )

    whois(
        "example.com",
        collect=True,
    )
"""

import mush

http = mush._load_internal("_http")
net = mush._load_internal("_net")

_BASE = "https://rdap.org/"

_HEADERS = {
    "User-Agent": "mush-whois/1.0",
    "Accept": "application/rdap+json,application/json",
}


def _http_connect(info, timeout=5000):
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


def _is_ipv4(value):
    parts = value.split(".")

    if len(parts) != 4:
        return False

    try:
        for part in parts:
            n = int(part)

            if n < 0 or n > 255:
                return False

        return True

    except Exception:
        return False


def _url(query):
    if _is_ipv4(query):
        return _BASE + "ip/" + query

    return _BASE + "domain/" + query


def _print_list(title, values):
    if values:
        print("{}:".format(title))

        for value in values:
            print("  {}".format(value))


def _print_events(events):
    if not events:
        return

    print("Events:")

    for event in events:
        action = event.get("eventAction")
        date = event.get("eventDate")

        if action and date:
            print(
                "  {}: {}".format(
                    action,
                    date,
                )
            )


def _print_nameservers(nameservers):
    if not nameservers:
        return

    print("Nameservers:")

    for ns in nameservers:
        name = ns.get("ldhName")

        if name:
            print("  {}".format(name))


def _print_entities(entities):
    if not entities:
        return

    print("Entities:")

    for entity in entities:
        handle = entity.get("handle")
        roles = entity.get("roles")

        if handle:
            print("  {}".format(handle))

        if roles:
            print(
                "    Roles: {}".format(
                    ", ".join(roles)
                )
            )


def _print_notices(notices):
    if not notices:
        return

    print("Notices:")

    for notice in notices:
        title = notice.get("title")

        if title:
            print("  {}".format(title))

        for line in notice.get(
            "description",
            [],
        ):
            print("    {}".format(line))


def _print_links(links):
    if not links:
        return

    print("Links:")

    for link in links:
        href = link.get("href")

        if href:
            print("  {}".format(href))


def _display(query, data, verbose):
    print(
        "Query: {}".format(
            query
        )
    )

    handle = data.get("handle")

    if handle:
        print(
            "Handle: {}".format(
                handle
            )
        )

    name = data.get("ldhName")

    if name:
        print(
            "Name: {}".format(
                name
            )
        )

    obj = data.get("objectClassName")

    if obj:
        print(
            "Class: {}".format(
                obj
            )
        )

    _print_list(
        "Status",
        data.get("status"),
    )

    _print_events(
        data.get("events")
    )

    if verbose:
        _print_nameservers(
            data.get("nameservers")
        )

        _print_entities(
            data.get("entities")
        )

        _print_notices(
            data.get("notices")
        )

        _print_links(
            data.get("links")
        )


def main(
    query,
    verbose=False,
    collect=False,
):
    try:
        response = http["request"](
            _url(query),
            headers=_HEADERS,
            connect=_http_connect,
        )

        try:
            if response.code() != 200:
                raise OSError(
                    response.status
                )

            data = response.json()

        finally:
            response.close()

        if collect:
            return data

        _display(
            query,
            data,
            verbose,
        )

        return None

    except Exception as e:
        print(
            "whois: {}: {}".format(
                query,
                e,
            )
        )

        return False
