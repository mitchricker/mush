# mush

A BusyBox-inspired Unix shell for MicroPython embedded devices.

mush provides a lightweight command-line environment for MicroPython boards, bringing familiar Unix-style utilities to resource-constrained hardware while keeping the full power of Python available.

## Features

- Filesystem tools:
  - ls
  - cd
  - pwd
  - cp
  - mv
  - rm
  - mkdir
  - touch
  - stat
  - tree

- Text processing:
  - cat
  - head
  - tail
  - grep
  - wc
  - uniq
  - base64
  - xxd
  - sha256sum

- Networking:
  - curl
  - ping
  - nc
  - nslookup
  - ntp
  - wifi

- System utilities:
  - uname
  - lscpu
  - free
  - df
  - sysinfo
  - date
  - reboot

- Built-in text editor:
  - edit

## Usage

Import mush:

    from mush import *

List available commands:

    man()

View documentation for a command:

    man("wifi")

Run commands directly:

    ls()
    wifi()
    curl("https://example.com")

## Python Integration

mush commands are regular MicroPython functions. They can be used alongside normal Python code, allowing shell-style utilities and application logic to be combined in the same environment.

Examples:

    files = ls()
    wifi("status")

    for item in find("/"):
        print(item)

    data = open("config.txt").read()

If you want mush commands to be always available on boot: you can save `from mush import *` to your `boot.py`.

## Design

mush is a collection of small Python modules designed for MicroPython environments.

Commands are intentionally lightweight and designed around embedded constraints:

- Streaming file operations
- Minimal memory usage
- Simple extension model
- Unix-inspired command interface

Adding a new command is as simple as adding another module.

## Creating Your Own Commands

mush commands are simple MicroPython modules. To create a new command, add a Python file to the mush command directory.

For example, create:

    mush/hello.py

with:

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

The command will then be available through mush:

    hello("world")

Command documentation is provided through `man()`:

    man("hello")

## Internal Modules

mush provides internal helper modules for common functionality. These modules are intended to keep commands small, consistent, and compatible with embedded hardware constraints.

### _fsio.py

`_fsio.py` provides streaming filesystem operations.

Use it when working with files that may be larger than available RAM.

Example:

    import mush._fsio as fsio

    for chunk in fsio.read_chunks("large_file.bin"):
        process(chunk)

Available helpers include:

- read_chunks()
- write_stream()
- copy()
- atomic_write()
- iter_lines()

Commands such as `cat`, `head`, `tail`, `xxd`, and `sha256sum` use these helpers to avoid loading entire files into memory.

### _sys.py

`_sys.py` provides system information helpers.

Use it instead of directly querying hardware APIs when writing system-related commands.

Example:

    import mush._sys as sysinfo

    memory = sysinfo.mem_info()

    filesystem = sysinfo.fs_info("/")

    cpu = sysinfo.cpu_info()

Available helpers include:

- mem_info()
- fs_info()
- cpu_info()
- uname_info()
- format_size()
- percent()
- summary()

Commands such as `df`, `lscpu`, and `sysinfo` build on these functions.

### _net.py

`_net.py` provides shared networking primitives for mush commands.

It handles common socket operations so individual commands do not need to duplicate connection setup, DNS resolution, timeout handling, TLS support or cleanup.

Example:

    import mush._net as net

    sock = net.tcp_connect("example.com", 80)

    sock.send(b"GET / HTTP/1.0\r\n\r\n")

    for data in net.recv_iter(sock):
        print(data)

    net.safe_close(sock)

Available helpers include:

- resolve()
- tcp_connect()
- udp_connect()
- tls_wrap()
- recv_iter()
- safe_close()

Networking commands such as `curl`, `ping`, `nc`, and `nslookup` use this layer to share common socket behavior.

## Requirements

- MicroPython
- Filesystem support
- Network-capable hardware for networking features

## License

MIT
