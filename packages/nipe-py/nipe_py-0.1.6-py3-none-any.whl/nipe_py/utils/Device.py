from collections import namedtuple


# * https://stackoverflow.com/questions/29030135/module-to-parse-a-simple-syntax-in-python
def read_release_file() -> namedtuple:
    with open("/etc/os-release") as f:
        keys, values = zip(
            *[
                (k.lower(), v.strip("'\""))
                for (k, v) in (line.strip().split("=", 1) for line in f.read().strip().split("\n"))
            ]
        )
    r = namedtuple("OSRelease", keys)(*values)
    return r


class Device:
    def __init__(self):
        config = read_release_file()
        id_like = getattr(config, "id_like", "")
        id_distro = getattr(config, "id", "ID")

        self.device = {"username": "debian-tor", "distribution": "debian"}

        if "fedora" in id_like.lower() or "fedora" in id_distro.lower():
            self.device["username"] = "toranon"
            self.device["distribution"] = "fedora"

        elif any(dist in id_like.lower() or dist in id_distro.lower() for dist in ["arch", "centos"]):
            self.device["username"] = "tor"
            self.device["distribution"] = "arch"

        elif "void" in id_distro.lower():
            self.device["username"] = "tor"
            self.device["distribution"] = "void"

    def get_device(self) -> dict:
        return self.device
