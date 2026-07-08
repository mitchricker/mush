# Mush

A BusyBox-inspired Unix shell for MicroPython embedded devices.

Mush provides a lightweight command-line environment for MicroPython boards, bringing familiar Unix-style utilities to resource-constrained hardware while keeping the full power of Python available.

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

Import Mush:

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

Mush commands are regular MicroPython functions. They can be used alongside normal Python code, allowing shell-style utilities and application logic to be combined in the same environment.

Examples:

    files = ls()
    wifi("status")

    for item in find("/"):
        print(item)

    data = open("config.txt").read()

Mush does not replace MicroPython but rather extends it with a familiar command-oriented interface.

## Design

Mush is a collection of small Python modules designed for MicroPython environments.

Commands are intentionally lightweight and designed around embedded constraints:

- Streaming file operations
- Minimal memory usage
- Simple extension model
- Unix-inspired command interface

Adding a new command is as simple as adding another module.

## Requirements

- MicroPython
- Filesystem support
- Network-capable hardware for networking features

## License

MIT
