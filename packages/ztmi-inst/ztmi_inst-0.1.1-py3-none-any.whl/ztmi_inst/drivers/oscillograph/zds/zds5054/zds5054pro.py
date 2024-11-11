from functools import cached_property
from ztmi_inst.drivers.driver import Driver
from ztmi_inst.drivers.oscillograph.osc_driver import OscillographDriver
from ztmi_inst.commands.zds.zds5054.zds5054_commands import ZDS5054Command


class _ZDS5054ProDriver(OscillographDriver):

    def __init__(self, host, port):
        # print("ZDS5054ProDriver Init")
        super().__init__(host, port)
        dev = self if isinstance(self, Driver) else None
        self._commands = ZDS5054Command(dev)
        self.__idn_string = self._commands.idn.read()
        self._dev_name = self.model

    @property
    def commands(self) -> ZDS5054Command:
        return self._commands

    @cached_property
    def manufacturer(self):
        return self.__idn_string.split(",")[0].strip()

    @cached_property
    def model(self):
        return self.__idn_string.split(",")[1].strip()

    @cached_property
    def serial(self):
        return self.__idn_string.split(",")[2].strip()

    @cached_property
    def version(self):
        return f"{self.__idn_string.split(",")[3].strip()} {self.__idn_string.split(",")[4].strip()}".strip()

    @cached_property
    def valid_channel(self):
        return 4


class ZDS5054ProDevice(_ZDS5054ProDriver):
    pass
