from nipe_py.engine.Start import Start
from nipe_py.engine.Stop import Stop


class Restart:
    def __init__(self):
        self.stop = Stop()

    def restart(self) -> bool:
        if self.stop.stop():
            start = Start()

            if start.start():
                return True
        return False
