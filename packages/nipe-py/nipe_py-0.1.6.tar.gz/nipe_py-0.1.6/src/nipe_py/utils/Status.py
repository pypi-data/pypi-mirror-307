import json

import requests
from rich import print
from rich.console import Console
from rich.panel import Panel

console = Console()

API_URL = "https://check.torproject.org/api/ip"


class Status:
    def __init__(self):
        self.status = False
        response = requests.get(API_URL)

        if response.status_code == 200:  # ignore: PLR2004
            data = json.loads(response.content)

            check_ip = data["IP"]
            check_tor = "true" if data["IsTor"] else "false"

            if check_tor == "true":
                print(Panel.fit(f"[magenta][+] Status: [green]Active[/green] \n[+] Ip: [/magenta][yellow]{check_ip}"))
                self.status = True
            else:
                print(Panel.fit(f"[magenta][+] Status: [red]Not Active[/red] \n[+] Ip: [/magenta][yellow]{check_ip}"))
                self.status = False
        else:
            print(
                Panel.fit("[red][!] ERROR: sorry, it was not possible to establish a connection to the server.[/red]")
            )
            self.status = False
