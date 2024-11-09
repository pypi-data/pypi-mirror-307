# KeePasste

## Introduction

Enters your credentials from KeePassXC for a value found on your primary clipboard.

Auto-Type in KeePassXC seems only supported on X11. This tool also works on Wayland
and automatically finds the correct values for any selected text.

## Installation

```
pipx install keepasste
```

## Configuration

```
[database]
filename = "/home/user/Documents/passwords.kdbx"
password = "a2V5cGFzc3RlMQ=="

[mappings]
"example.com" = "/example.com/user"
```

Put in your KeePass database filename and password in the `database` section.

Create your mappings to entries in your keepass database.

## Usage

Select a text to put it on your primary clipboard. Then execute `keepasste Username` to
input the Username attribute of the mapped value from your KeePass database.
