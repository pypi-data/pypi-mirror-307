import subprocess
from pathlib import Path

from rich.console import Console

from nipe_py.utils.Device import Device

console = Console()


class Stop:
    def __init__(self):
        device = Device()
        self.device = device.get_device()
        tables = ["nat", "filter"]
        self.stop_tor = "systemctl stop tor"

        if self.device["distribution"] == "void":
            self.start_tor = "sv stop tor > /dev/null"

        for table in tables:
            subprocess.call(f"iptables -t {table} -F OUTPUT", shell=True)
            subprocess.call(f"iptables -t {table} -F OUTPUT", shell=True)

        if Path("/etc/init.d/tor").exists():
            self.stop_tor = "/etc/init.d/tor stop > /dev/null"

    def stop(self) -> bool:
        try:
            subprocess.check_call(self.stop_tor, shell=True)
            subprocess.check_call("$(which killall) tor > /dev/null", shell=True)
            return True
        except Exception:
            console.print_exception()
            return False
