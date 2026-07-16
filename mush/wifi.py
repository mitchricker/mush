__doc__ = """
NAME
    wifi - WiFi management utility

SYNOPSIS
    wifi("scan", collect=False)
    wifi("connect", ssid, password)
    wifi("disconnect")
    wifi("status")
    wifi("config", ip=..., netmask=..., gateway=..., dns=...)

DESCRIPTION
    Lightweight wrapper around the MicroPython network module.

    Returns:
        scan:
            collect=True:
                list of tuples:
                (
                    ssid,
                    bssid,
                    channel,
                    rssi,
                    security,
                    hidden
                )

            collect=False:
                None on success

        status:
            (
                connected,
                mac,
                ip,
                netmask,
                gateway,
                dns
            )

        connect:
            None on success
            False on failure

        disconnect:
            None on success
            False on failure

        config:
            (
                ip,
                netmask,
                gateway,
                dns
            )

        False on failure

EXAMPLES
    wifi("scan")

    wifi(
        "scan",
        collect=True,
    )

    wifi(
        "connect",
        "MyWifi",
        "password",
    )

    wifi("status")

    wifi(
        "config",
        ip="192.168.1.50",
        netmask="255.255.255.0",
        gateway="192.168.1.1",
        dns="8.8.8.8",
    )
"""

import network
import time


_SECURITY = {
    0: "OPEN",
    1: "WEP",
    2: "WPA-PSK",
    3: "WPA2-PSK",
    4: "WPA/WPA2-PSK",
}


def _get_sta():
    wlan = network.WLAN(
        network.STA_IF
    )

    if not wlan.active():
        wlan.active(True)

    return wlan


def _fmt_mac(mac):
    return ":".join(
        "{:02X}".format(b)
        for b in mac
    )


def _decode_ssid(ssid):
    if isinstance(ssid, bytes):
        return ssid.decode(
            "utf-8",
            "ignore",
        )

    return ssid


def _status(wlan):
    connected = wlan.isconnected()

    mac = None
    ip = None
    mask = None
    gateway = None
    dns = None

    try:
        mac = _fmt_mac(
            wlan.config("mac")
        )

    except Exception:
        pass

    if connected:
        (
            ip,
            mask,
            gateway,
            dns,
        ) = wlan.ifconfig()

    return (
        connected,
        mac,
        ip,
        mask,
        gateway,
        dns,
    )


def _print_status(result):
    (
        connected,
        mac,
        ip,
        mask,
        gateway,
        dns,
    ) = result

    print(
        "Connected:",
        connected,
    )

    if mac:
        print(
            "MAC:",
            mac,
        )

    if connected:
        print(
            "IP:",
            ip,
        )

        print(
            "Netmask:",
            mask,
        )

        print(
            "Gateway:",
            gateway,
        )

        print(
            "DNS:",
            dns,
        )


def main(
    cmd="status",
    *args,
    collect=False,
    **kwargs,
):
    try:
        wlan = _get_sta()

    except Exception as e:
        print(
            "wifi: {}".format(
                e
            )
        )

        return False


    if cmd == "connect":

        if len(args) < 2:
            print(
                "wifi: connect requires ssid and password"
            )

            return False

        ssid = args[0]
        password = args[1]

        try:
            print(
                "Connecting to {}...".format(
                    ssid
                )
            )

            wlan.connect(
                ssid,
                password,
            )

            for _ in range(20):

                if wlan.isconnected():

                    print(
                        "Connected"
                    )

                    return None

                time.sleep(
                    0.5
                )

        except Exception as e:

            print(
                "wifi: {}".format(
                    e
                )
            )

            return False

        print(
            "wifi: connection failed"
        )

        return False


    if cmd == "disconnect":

        try:
            wlan.disconnect()

            print(
                "Disconnected"
            )

            return None

        except Exception as e:

            print(
                "wifi: {}".format(
                    e
                )
            )

            return False


    if cmd == "status":

        try:
            result = _status(
                wlan
            )

            if not collect:
                _print_status(
                    result
                )

            return result

        except Exception as e:

            print(
                "wifi: {}".format(
                    e
                )
            )

            return False


    if cmd == "config":

        try:
            current = wlan.ifconfig()

            result = (
                kwargs.get(
                    "ip",
                    current[0],
                ),

                kwargs.get(
                    "netmask",
                    current[1],
                ),

                kwargs.get(
                    "gateway",
                    current[2],
                ),

                kwargs.get(
                    "dns",
                    current[3],
                ),
            )

            wlan.ifconfig(
                result
            )

            print(
                "Network configuration updated"
            )

            return result

        except Exception as e:

            print(
                "wifi: {}".format(
                    e
                )
            )

            return False


    if cmd == "scan":

        try:
            aps = sorted(
                wlan.scan(),
                key=lambda ap: ap[3],
                reverse=True,
            )

            results = []

            for (
                ssid,
                bssid,
                channel,
                rssi,
                security,
                hidden,
            ) in aps:

                item = (
                    _decode_ssid(ssid),
                    _fmt_mac(bssid),
                    channel,
                    rssi,
                    _SECURITY.get(
                        security,
                        str(security),
                    ),
                    bool(hidden),
                )

                if collect:
                    results.append(
                        item
                    )

                else:
                    print(
                        item
                    )

            if collect:
                return results

            return None

        except Exception as e:

            print(
                "wifi: {}".format(
                    e
                )
            )

            return False


    print(
        "wifi: unknown command:",
        cmd,
    )

    return False
