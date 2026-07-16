__doc__ = """
NAME
    sdmount - mount an SD card

SYNOPSIS
    sdmount(path="/sd", sck=18, mosi=23, miso=19,
            cs=4, spi=2, baudrate=10000000)

DESCRIPTION
    Mounts an SD card filesystem using os.mount().

    Attempts to use machine.SDCard first.
    If the firmware does not support configurable SD pins,
    falls back to SPI SD support when available.

    Defaults are for ESP32 boards using the common VSPI mapping.

    Options:
        path:
            Mount point.

        sck:
            SPI clock pin.

        mosi:
            SPI MOSI pin.

        miso:
            SPI MISO pin.

        cs:
            SD chip select pin.

        spi:
            SPI bus number.

        baudrate:
            SPI clock frequency.

    Returns:
        True    - success
        False   - failure

EXAMPLES
    sdmount()

    sdmount(
        path="/card",
    )

    sdmount(
        cs=5,
    )

    sdmount(
        path="/storage",
        sck=14,
        cs=15,
    )
"""

import os
import machine


def _mount(card, path):
    os.mount(
        card,
        path,
    )

    print(
        "mounted SD at {}".format(
            path
        )
    )

    return True


def main(
    path="/sd",
    sck=18,
    mosi=23,
    miso=19,
    cs=4,
    spi=2,
    baudrate=10000000,
):
    card = None

    if not hasattr(machine, "SDCard"):
        print("sdmount: machine.SDCard unavailable")

    else:
        try:
            card = machine.SDCard(
                slot=spi,
                sck=machine.Pin(sck),
                mosi=machine.Pin(mosi),
                miso=machine.Pin(miso),
                cs=machine.Pin(cs),
                baudrate=baudrate,
            )

        except TypeError:
            try:
                card = machine.SDCard(
                    slot=spi,
                )

            except Exception:
                pass

        except Exception:
            pass

    if card is None:
        try:
            import sdcard

            bus = machine.SPI(
                spi,
                baudrate=baudrate,
                polarity=0,
                phase=0,
                sck=machine.Pin(sck),
                mosi=machine.Pin(mosi),
                miso=machine.Pin(miso),
            )

            card = sdcard.SDCard(
                bus,
                machine.Pin(cs),
            )

        except ImportError:
            print("sdmount: no compatible SD driver")

        except Exception as e:
            print(
                "sdmount: SPI SD init failed:",
                e,
            )

    if card is None:
        return False

    try:
        return _mount(
            card,
            path,
        )

    except Exception as e:
        print(
            "sdmount: mount failed:",
            e,
        )

        return False
