import subprocess
from pathlib import Path
from typing import Union

from rich.console import Console

from nipe_py.utils.Device import Device


def get_config_path() -> Union[Path, FileNotFoundError]:
    base_path = Path(__file__).resolve().parent

    # Check if the package is installed in site-packages (pip install)
    site_packages_path = base_path.parents[1] / ".configs"
    if site_packages_path.exists():
        return site_packages_path

    # Check if the package is installed in a virtual environment (pip install -e .)
    local_package_path = base_path.parents[2] / ".configs"
    if local_package_path.exists():
        return local_package_path

    # If neither path exists, raise an error or return a default value
    raise FileNotFoundError("Configuration path not found")


config_path = get_config_path()


console = Console()


class Start:
    def __init__(self):
        device = Device()
        self.device = device.get_device()
        self.dns_port = "9061"
        self.transfer_port = "9051"
        self.table = ["nat", "filter"]
        self.network = "10.66.0.0/255.255.0.0"
        self.start_tor = "systemctl start tor"

        if self.device["distribution"] == "void":
            self.start_tor = "sv start tor > /dev/null"

        elif Path("/etc/init.d/tor").exists():
            self.start_tor = "/etc/init.d/tor start > /dev/null"

    def start(self) -> bool:
        try:
            subprocess.check_call(
                f"tor -f {config_path}/{self.device['distribution']}-torrc > /dev/null",
                shell=True,
            )
            subprocess.check_call(self.start_tor, shell=True)

            for t in self.table:
                self.target = "ACCEPT"

                if t == "nat":
                    self.target = "RETURN"

                subprocess.check_call(f"iptables -t {t} -F OUTPUT", shell=True)
                subprocess.check_call(
                    f"iptables -t {t} -A OUTPUT -m state --state ESTABLISHED -j {self.target}",
                    shell=True,
                )
                subprocess.check_call(
                    f"iptables -t {t} -A OUTPUT -m owner --uid {self.device['username']} -j {self.target}",
                    shell=True,
                )

                self.match_dns_port = self.dns_port

                if t == "nat":
                    self.target = f"REDIRECT --to-ports {self.dns_port}"
                    self.match_dns_port = "53"

                subprocess.check_call(
                    f"iptables -t {t} -A OUTPUT -p udp --dport {self.match_dns_port} -j {self.target}",
                    shell=True,
                )
                subprocess.check_call(
                    f"iptables -t {t} -A OUTPUT -p tcp --dport {self.match_dns_port} -j {self.target}",
                    shell=True,
                )

                if t == "nat":
                    self.target = f"REDIRECT --to-ports {self.transfer_port}"

                subprocess.check_call(
                    f"iptables -t {t} -A OUTPUT -d {self.network} -p tcp -j {self.target}",
                    shell=True,
                )

                if t == "nat":
                    self.target = "RETURN"

                subprocess.check_call(
                    f"iptables -t {t} -A OUTPUT -d 127.0.0.1/8    -j {self.target}",
                    shell=True,
                )
                subprocess.check_call(
                    f"iptables -t {t} -A OUTPUT -d 192.168.0.0/16 -j {self.target}",
                    shell=True,
                )
                subprocess.check_call(
                    f"iptables -t {t} -A OUTPUT -d 172.16.0.0/12  -j {self.target}",
                    shell=True,
                )
                subprocess.check_call(
                    f"iptables -t {t} -A OUTPUT -d 10.0.0.0/8     -j {self.target}",
                    shell=True,
                )

                if t == "nat":
                    self.target = f"REDIRECT --to-ports {self.transfer_port}"

                subprocess.check_call(f"iptables -t {t} -A OUTPUT -p tcp -j {self.target}", shell=True)

            subprocess.check_call("iptables -t filter -A OUTPUT -p udp -j REJECT", shell=True)
            subprocess.check_call("iptables -t filter -A OUTPUT -p icmp -j REJECT", shell=True)

            subprocess.check_call("sysctl -w net.ipv6.conf.all.disable_ipv6=1 >/dev/null", shell=True)
            subprocess.check_call("sysctl -w net.ipv6.conf.default.disable_ipv6=1 >/dev/null", shell=True)

            return True
        except subprocess.CalledProcessError:
            console.print_exception()
            return False
