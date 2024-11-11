# ZDS系列根命令类定义
from commands.command import *


class RootCommand(BaseCommand):
    """
    ZDS系列示波器ROOT命令树构建。

    属性：
        - ``.auto_setup``: ``AUTosetup`` 命令；
        - ``.clear``: ``CLEar`` 命令；
        - ``.default``: ``DEFault`` 命令;
        - ``.print``: ``PRINt`` 命令;
        - ``.run``: ``RUN`` 命令;
        - ``.single``: ``SINGle`` 命令;
        - ``.stop``: ``STOP`` 命令;
        - ``.tl_half``: ``TLHAlf`` 命令。
    """

    def __init__(self, dev):
        super().__init__(dev, "")
        self._auto_setup = CommandWriteNoValue(dev, f":AUTosetup")
        self._clear = CommandWriteNoValue(dev, ":CLEar")
        self._default = CommandWriteNoValue(dev, ":DEFault")
        self._print = CommandWriteNoValue(dev, ":PRINt")
        self._run = CommandWriteNoValue(dev, ":RUN")
        self._single = CommandWriteNoValue(dev, ":SINGle")
        self._stop = CommandWriteNoValue(dev, ":STOP")
        self._tl_half = CommandWriteNoValue(dev, ":TLHAlf")

    @property
    def auto_setup(self):
        return self._auto_setup

    @property
    def clear(self):
        return self._clear

    @property
    def default(self):
        return self._default

    @property
    def print(self):
        return self._print

    @property
    def run(self):
        return self._run

    @property
    def single(self):
        return self._single

    @property
    def stop(self):
        return self._stop

    @property
    def tl_half(self):
        return self._tl_half
