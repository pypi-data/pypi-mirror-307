from drivers.driver import Driver
from functools import cached_property
from commands.DMM6000.dmm6000_commands import DMM6000Command


class _DMM6000Driver(Driver):

    def __init__(self, host, port):
        super().__init__(host, port)
        dev = self if isinstance(self, Driver) else None
        self._commands = DMM6000Command(dev)
        self.__idn_string = self._commands.idn.read()
        self._dev_name = self.model
        pass

    @property
    def commands(self) -> DMM6000Command:
        return self._commands

    @cached_property
    def manufacturer(self):
        return self.__idn_string.split(" ")[0].strip()

    @cached_property
    def model(self):
        return self.__idn_string.split(" ")[1].strip()

    @cached_property
    def serial(self):
        return self.__idn_string.split(" ")[2].strip()

    @cached_property
    def version(self):
        return f"{self.__idn_string.split(" ")[3].strip()}".strip()


class DMM6000Device(_DMM6000Driver):
    pass
