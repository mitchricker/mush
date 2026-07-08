__doc__ = """
NAME
    wifi - WiFi management utility

SYNOPSIS
    wifi("scan")
    wifi("connect", ssid, password)
    wifi("disconnect")
    wifi("status")
    wifi("config", ip=..., netmask=..., gateway=..., dns=...)

DESCRIPTION
    Lightweight wrapper around the MicroPython network module.

    Supports scanning for nearby access points, connecting to
    wireless networks, viewing connection status, disconnecting,
    and configuring the station interface.

EXAMPLES
    wifi("scan")

    wifi("connect", "MyWiFi", "password123")

    wifi("status")

    wifi(
        "config",
        ip="192.168.1.50",
        netmask="255.255.255.0",
        gateway="192.168.1.1",
        dns="1.1.1.1",
    )

    wifi("disconnect")
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
    wlan = network.WLAN(network.STA_IF)

    if not wlan.active():
        wlan.active(True)

    return wlan


def _fmt_mac(mac):
    return ":".join("{:02X}".format(b) for b in mac)


def main(cmd="status", *args, **kwargs):
    wlan = _get_sta()

    if cmd == "connect":
        if len(args) < 2:
            print("wifi: connect requires ssid and password")
            return

        ssid, password = args[:2]

        print("Connecting to '{}'...".format(ssid))
        wlan.connect(ssid, password)

        for _ in range(20):
            if wlan.isconnected():
                break
            time.sleep(0.5)

        if wlan.isconnected():
            print("Connected.")
            print("IP:", wlan.ifconfig()[0])
        else:
            print("Connection failed.")

    elif cmd == "disconnect":
        wlan.disconnect()
        print("Disconnected.")

    elif cmd == "status":
        print("Connected :", wlan.isconnected())

        try:
            print("MAC       :", _fmt_mac(wlan.config("mac")))
        except Exception:
            pass

        if wlan.isconnected():
            ip, mask, gateway, dns = wlan.ifconfig()

            print("IP        :", ip)
            print("Netmask   :", mask)
            print("Gateway   :", gateway)
            print("DNS       :", dns)

    elif cmd == "config":
        ip, mask, gateway, dns = wlan.ifconfig()

        wlan.ifconfig((
            kwargs.get("ip", ip),
            kwargs.get("netmask", mask),
            kwargs.get("gateway", gateway),
            kwargs.get("dns", dns),
        ))

    elif cmd == "scan":
        print(
            "{:<24} {:>6} {:>4} {:<13} {:<6} {}".format(
                "SSID",
                "RSSI",
                "CH",
                "SECURITY",
                "HIDDEN",
                "BSSID",
            )
        )
        print("-" * 67)

        aps = sorted(
            wlan.scan(),
            key=lambda ap: ap[3],
            reverse=True,
        )

        for ssid, bssid, channel, rssi, sec, hidden in aps:
            if isinstance(ssid, bytes):
                ssid = ssid.decode("utf-8", "ignore")

            blank_ssid = not ssid

            if blank_ssid:
                display_ssid = "<hidden>"
            else:
                display_ssid = ssid

            try:
                mac = _fmt_mac(bssid)
            except Exception:
                mac = "?"

            if hidden:
                hidden_text = "yes"
            elif blank_ssid:
                hidden_text = "blank"
            else:
                hidden_text = "no"

            print(
                "{:<24} {:>6} {:>4} {:<13} {:<6} {}".format(
                    display_ssid[:24],
                    rssi,
                    channel,
                    _SECURITY.get(sec, str(sec)),
                    hidden_text,
                    mac,
                )
            )

    else:
        print("wifi: unknown command:", cmd)
