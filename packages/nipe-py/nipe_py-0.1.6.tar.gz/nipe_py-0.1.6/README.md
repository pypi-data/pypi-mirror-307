# nipe_py

<p align="center">
    <img src="./assets/banner.png">
</p>



<div align="center">

[![Python](https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white)](https://www.python.org/) [![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch) [![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF.svg?style=flat&logo=GitHub-Actions&logoColor=white)](https://github.com/features/actions)

[![PyPI version](https://img.shields.io/pypi/v/nipe_py.svg)](https://pypi.org/project/nipe_py)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nipe_py)](https://pypi.org/project/nipe_py/)
[![GitHub license](https://img.shields.io/github/license/aviksaikat/nipe_py?style=flat&color=1573D5)](https://github.com/aviksaikat/nipe_py/blob/main/LICENSE)

</div>

---

**Documentation**: <a href="https://aviksaikat.github.io/nipe_py/" target="_blank">https://aviksaikat.github.io/nipe_py/</a>

**Source Code**: <a href="https://github.com/aviksaikat/nipe_py" target="_blank">https://github.com/aviksaikat/nipe_py</a>

---

Python version of [nipe](https://github.com/htrgouvea/nipe): An engine to make Tor Network your default gateway.

## Installation

```sh
pip install nipe_py
```

- You need to have tor installed & tor should be running. Confirm it by running

```sh
# this will start the tor service if not already running. If running then it'll restart it.
sudo systemctl restart tor
```

## Usage
```sh
$ nipe --help
Usage: nipe [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  install  Install dependencies
  restart  Restart the Nipe circuit
  start    Start routing
  status   See status
  stop     Stop routing
  version  Show Version
```

## Demo
![](./assets/demo.gif)

## License

This project is licensed under the terms of the [MIT](./LICENSE) license.
