from ztmi_inst.drivers.driver import Driver
from functools import cached_property
from abc import abstractmethod, ABC


class OscillographDriver(Driver, ABC):
    """Base Driver for Oscillograph"""

    @cached_property
    @abstractmethod
    def valid_channel(self):
        """返回支持的通道数，需具体仪器类实现"""
        pass
