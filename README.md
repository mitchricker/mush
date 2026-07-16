# Mitch's Micro Shell (mush)

A BusyBox-inspired Unix shell for MicroPython embedded devices.

mush provides a lightweight command-line environment for MicroPython boards, bringing familiar Unix-style utilities to resource-constrained hardware while keeping the full power of Python available.

---

# Table of Contents

* [Overview](#overview)
* [Installation](#installation)
* [Usage](#usage)
* [Available Commands](#available-commands)
* [Command Return Values](#command-return-values)
* [Python Integration](#python-integration)
* [Internal Modules](#internal-modules)
* [Requirements](#requirements)
* [License](#license)

---

# Overview

mush is a collection of small Python modules designed to provide a familiar Unix-style environment for MicroPython devices.

It is inspired by BusyBox: commands are lightweight, independent modules that share common internal helpers.

The design goals are:

* Low memory usage
* Streaming file operations
* Simple extension model
* Hardware-friendly behavior
* Python-native integration
* Consistent command interfaces

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

# Command return values

mush commands support both interactive shell use and Python scripting.

By default:

* Commands print their output.
* Successful commands return `None`.
* Errors return `False`.

Example:

```text
mkdir("test")
```

prints:

```text
created: test
```

and returns:

```text
None
```

## Collection mode

Commands that generate useful data support `collect=True`.

With collection enabled, output is returned instead of only displayed.

Examples:

```text
date(collect=True)
```

returns:

```text
"2026-07-16 08:26:57"
```

```text
stat("boot.py", collect=True)
```

returns:

```text
("boot.py", 161, 32768, "file")
```

```text
find("/flash", collect=True)
```

returns a list of matching paths.

General rule:

* Normal use: print output, return `None`
* `collect=True`: return data
* Failure: return `False`

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
* `iter_lines_reverse`
* `output`

Commands such as:

* `cat`
* `head`
* `tail`
* `xxd`
* `sha256sum`
* `md5sum`
* `gzip`

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

use this layer.

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

use this layer.

---

## `_http`

`_http` provides HTTP client helpers.

Available features:

* URL parsing
* HTTP requests
* response handling
* redirects
* header processing

Commands such as:

* `curl`
* `wget`

use this layer.

---

## `_ntp`

`_ntp` provides SNTP synchronization helpers.

Available features:

* Default NTP server configuration
* Clock synchronization

Commands such as:

* `ntp`
* `ntpd`

use this layer.

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
