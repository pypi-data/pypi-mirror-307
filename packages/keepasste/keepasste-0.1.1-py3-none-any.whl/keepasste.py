import subprocess
import tomllib
import base64
import os.path
import sys


def main():
    pasted = subprocess.check_output(["wl-paste", "--primary"], encoding="utf8")[:-1]
    with open(os.path.expanduser("~/.config/keepasste/config.toml"), "rb") as f:
        config = tomllib.load(f)
    key = config["mappings"][pasted]

    p = subprocess.Popen(
        [
            "keepassxc-cli",
            "show",
            "-s",
            "-a",
            sys.argv[1],
            config["database"]["filename"],
            key,
        ],
        encoding="utf8",
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    value = p.communicate(
        base64.b64decode(config["database"]["password"]).decode("utf8")
    )[0][:-1]

    subprocess.check_call(
        [
            "sudo",
            "/usr/bin/injectinput",
            value.replace("\\", "\\\\") + "\\r"
        ]
    )
