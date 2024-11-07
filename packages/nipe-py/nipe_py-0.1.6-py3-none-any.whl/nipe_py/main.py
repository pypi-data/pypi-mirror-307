import click
from rich import print
from rich.panel import Panel

from nipe_py import Install, Restart, Start, Status, Stop, __version__


@click.group()
def cli():
    pass


@cli.command()
def install():
    """Install dependencies"""
    Install()


@cli.command()
def start():
    """Start routing"""
    st = Start()
    st.start()
    print(Panel("[+] [green]nipe has been started...."))


@cli.command()
def stop():
    """Stop routing"""
    stop = Stop()
    stop.stop()
    print(Panel("[+] [red]nipe has been stopped...."))


@cli.command()
def restart():
    """Restart the Nipe circuit"""
    rst = Restart()
    rst.restart()
    print(Panel("[+] [red]nipe has been restated...."))


@cli.command()
def status():
    """See status"""
    Status()


@cli.command()
def version():
    """Show Version"""
    print(Panel(f"[green]Version: [yellow]{__version__}"))


if __name__ == "__main__":
    cli()
