# Mitch's Micro Shell (mush)

A BusyBox-inspired Unix shell for MicroPython embedded devices.

mush provides a lightweight command-line environment for MicroPython boards, bringing familiar Unix-style utilities to resource-constrained hardware while keeping the full power of Python available.

---

# Table of Contents

* [Overview](#overview)
* [Installation](#installation)
* [Usage](#usage)
* [Available Commands](#available-commands)
* [Python Integration](#python-integration)
* [Internal Modules](#internal-modules)
* [Requirements](#requirements)
* [License](#license)

---

# Overview

mush is a collection of small Python modules designed to provide a familiar Unix-style environment on MicroPython devices.

It is inspired by BusyBox: commands are lightweight, independent modules that share common internal helpers.

The design goals are:

- Low memory usage
- Streaming file operations
- Simple extension model
- Hardware-friendly behavior
- Python-native integration

[Back to top](#mitchs-micro-shell-mush)

---

# Features

## Filesystem Utilities

- `ls`
- `cd`
- `pwd`
- `cp`
- `mv`
- `rm`
- `mkdir`
- `touch`
- `stat`
- `tree`

## Text Processing

- `cat`
- `tac`
- `nl`
- `head`
- `tail`
- `grep`
- `wc`
- `uniq`
- `cut`
- `strings`
- `base64`
- `xxd`
- `sha256sum`

## Networking

- `wifi` *(requires MicroPython network support and wireless-capable hardware)*
- `curl`
- `wget`
- `ping`
- `nc`
- `nslookup`
- `ntp`

## Compression

- `gzip` *(firmware dependent; requires MicroPython deflate compression support)*
- `gunzip`

## System Utilities

- `uname`
- `lscpu`
- `free`
- `df`
- `sysinfo`
- `find`
- `date`
- `cal`
- `reboot`

## Editor

- `edit`

[Back to top](#mitchs-micro-shell-mush)

---

# Installation

Copy the `mush` package directory onto your MicroPython filesystem.

Example layout:

```
/mush
    __init__.py
    ls.py
    grep.py
    curl.py
    wifi.py
```

Commands are discovered automatically when mush starts.

[Back to top](#mitchs-micro-shell-mush)

---

# Usage

Import mush:

```
from mush import *
```

List available commands:

```
man()
```

View documentation for a command:

```
man("wifi")
```

Run commands directly:

```
ls()
wifi()
curl("https://example.com")
```

[Back to top](#mitchs-micro-shell-mush)

---

# Available Commands

Commands are implemented as individual Python modules.

Current commands:

## Filesystem

* `cd`
* `cp`
* `du`
* `find`
* `ls`
* `mkdir`
* `mv`
* `pwd`
* `rm`
* `stat`
* `touch`
* `tree`

## Text

* `base64`
* `cat`
* `cut`
* `grep`
* `head`
* `nl`
* `strings`
* `tail`
* `tac`
* `uniq`
* `wc`
* `xxd`

## Data and Checksums

* `cmp`
* `ipcalc`
* `md5sum`
* `sha256sum`

## Networking

* `curl`
* `httpd`
* `mdnsd`
* `nc`
* `nslookup`
* `ntp`
* `ntpd`
* `ping`
* `wget`
* `wifi`
* `whois`

Networking commands require MicroPython network support and appropriate hardware.

## System

* `cal`
* `clear`
* `date`
* `df`
* `free`
* `lscpu`
* `reboot`
* `runtime`
* `sysinfo`
* `uname`

## Compression

* `gzip`
* `gunzip`

Compression support depends on available MicroPython modules.
Decompression should be supported in more cases.

## Hardware

* `sdmount`
* `umount`

## Utilities

* `edit`
* `man`

Each command provides:

* A `main()` function
* `__doc__` documentation used by `man()`
* A callable interface through mush

Commands are loaded on demand to reduce memory usage.

Example command layout:

```
mush/
    hello.py
```

Example command:

```
__doc__ = """
NAME
    hello - print a greeting

SYNOPSIS
    hello(name)

EXAMPLES
    hello("world")
"""

def main(name="world"):
    print("Hello, {}".format(name))
```

The command becomes available automatically:

```
hello("world")
```

Command documentation is available through:

```
man("hello")
```

[Back to top](#mitchs-micro-shell-mush)

---

# Python Integration

mush commands are regular MicroPython functions and can be called from normal Python code.

mush commands can be used from scripts just like any other function:

    from mush import sysinfo, runtime

    sysinfo()

    runtime()

[Back to top](#mitchs-micro-shell-mush)

---

# Internal Modules

mush provides internal helper modules used by commands.

These modules are not directly imported by commands. Instead, they are loaded through the mush internal loader:

```
helper = mush._load_internal("_name")
```

The loader returns a dictionary of helper functions. This keeps internal dependencies lightweight and consistent across commands.

---

## `_fsio`

`_fsio` provides streaming filesystem helpers for commands that need to process files without loading entire files into memory.

Available helpers:

* `read_chunks`
* `write_stream`
* `copy`
* `atomic_write`
* `iter_lines`

Commands such as:

- `cat`
- `head`
- `tail`
- `xxd`
- `sha256sum`

use these helpers to minimize memory usage.

---

## `_sys`

`_sys` provides system information helpers.

Available helpers:

* `mem_info`
* `fs_info`
* `cpu_info`
* `reset_cause`
* `uname_info`
* `format_size`
* `percent`
* `summary`

Commands such as:

* `df`
* `free`
* `lscpu`
* `sysinfo`

use these helpers.

---

## `_net`

`_net` provides shared networking primitives for commands that require sockets, DNS resolution, TLS support, or connection cleanup.

Available helpers:

* `resolve`
* `tcp_connect`
* `udp_connect`
* `tls_wrap`
* `recv_iter`
* `safe_close`

Commands such as:

* `curl`
* `wget`
* `ping`
* `nc`
* `nslookup`
* `whois`

use this layer to share common socket behavior.

[Back to top](#mitchs-micro-shell-mush)

---

# Requirements

* MicroPython v1.21 or newer
* Filesystem support
* Network-capable hardware for networking features

Optional MicroPython modules:

* `network`
* `ssl`
* `deflate`
* `machine`
* `socket`

[Back to top](#mitchs-micro-shell-mush)

---

# License

MIT License

[Back to top](#mitchs-micro-shell-mush)
