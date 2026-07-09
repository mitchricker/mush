__doc__ = """
NAME
    reboot - restart the system

SYNOPSIS
    reboot()

DESCRIPTION
    Performs a software reset of the device. This is equivalent
    to pressing the reset button. The shell and all running
    programs will terminate and the board will reboot.

EXAMPLES
    reboot()
"""
import machine
def main():
    print("Rebooting...")
    machine.reset()

