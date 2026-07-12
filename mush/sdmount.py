__doc__ = """
NAME
    sdmount - mount an SD card

SYNOPSIS
    sdmount([path="/sd"], [sck=18], [mosi=23], [miso=19], [cs=4], [spi=2])

DESCRIPTION
    Mounts an SPI SD card.

    Defaults are for ESP32 boards using the common VSPI mapping.
    Pins can be configured individually for different board layouts.

EXAMPLES
    sdmount()
    sdmount(path="/card")
    sdmount(cs=5)
    sdmount(path="/storage", sck=14, cs=15)
"""

import os
import machine


def main(path="/sd",
         sck=18,
         mosi=23,
         miso=19,
         cs=4,
         spi=2,
         baudrate=10000000):

    if not hasattr(machine, "SDCard"):
        print("sdmount: machine.SDCard unavailable")
        return False

    try:
        card = machine.SDCard(
            slot=spi,
            sck=machine.Pin(sck),
            mosi=machine.Pin(mosi),
            miso=machine.Pin(miso),
            cs=machine.Pin(cs),
            baudrate=baudrate,
        )

    except OSError as e:
        print("sdmount: SDCard init failed:", e)
        return False

    try:
        os.mount(card, path)
        print("mounted SD at {}".format(path))
        return True

    except OSError as e:
        print("sdmount: mount failed:", e)
        return False
