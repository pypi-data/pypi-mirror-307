import subprocess
from pathlib import Path

from rich import print
from rich.console import Console
from rich.panel import Panel

from nipe_py.utils.Device import Device

console = Console()


class Install:
    def __init__(self):
        device = Device()
        self.device = device.get_device()
        self.stop_tor = "systemctl stop tor"

        self.install = {
            "debian": "apt-get install -y tor iptables",
            "fedora": "dnf install -y tor iptables",
            "centos": "yum -y install epel-release tor iptables",
            "void": "xbps-install -y tor iptables",
            "arch": "pacman -S --noconfirm tor iptables",
        }

        if self.device["distribution"] == "void":
            self.stop_tor = "sv stop tor > /dev/null"
        if Path("/etc/init.d/tor").exists():
            self.stop_tor = "/etc/init.d/tor stop > /dev/null"
        try:
            subprocess.call(
                f"{self.install[self.device['distribution']]} && {self.stop_tor}",
                shell=True,
            )
            print(Panel.fit("[+][green]nipe has been installed...."))
        except Exception as _:
            console.print_exception()
