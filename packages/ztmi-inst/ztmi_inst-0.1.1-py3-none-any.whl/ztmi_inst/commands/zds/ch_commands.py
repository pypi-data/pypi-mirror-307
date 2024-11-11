# ZDS系列通道命令类定义
import re
from commands.command import *


def _bool_arg_check(value: Any) -> bool:
    if isinstance(value, bool):
        return True
    if isinstance(value, str) and value.upper() in ("ON", "OFF"):
        return True
    if isinstance(value, int) and value in (0, 1):
        return True
    return False


def _digital_arg_check(value: Any) -> bool:
    return isinstance(value, float) or isinstance(value, int)


class ValidChannelCheck(BaseCommand):
    """
    通道校验，检查通道是否超过支持的通道数
    """
    def __init__(self, dev, command_syntax):
        super().__init__(dev, command_syntax)
        # print("ValidChannelCheck Init")
        valid_ch_num = dev.valid_channel
        if (digital := re.compile(r"(\d+)(,?)$").search(command_syntax)) is not None:
            channel = int(digital.group(1))
        else:
            raise ValueError(f"Invalid channel syntax: {command_syntax}")
        if channel not in range(1, valid_ch_num + 1):
            raise ValueError(f"Invalid channel number: {command_syntax}")


class ChannelDisplay(CommandRead, CommandWrite):
    """
    模拟通道开关命令
    """
    def write(self, value: Any) -> str:
        if _bool_arg_check(value):
            return super().write(value)
        raise ValueError(f"Channel Display Invalid value: {value}")


class ChannelVernier(CommandRead, CommandWrite):
    """
    模拟通道垂直灵敏度档位切换命令
    """
    def write(self, value: Any) -> str:
        if _bool_arg_check(value):
            return super().write(value)
        raise ValueError(f"Channel Vernier Invalid value: {value}")


class ChannelScale(CommandRead, CommandWrite):
    """
    模拟通道垂直灵敏度配置命令
    """
    def write(self, value: Any) -> str:
        if _digital_arg_check(value):
            return super().write(value)
        raise ValueError(f"Channel Scale Invalid value: {value}")


class ChannelOffset(CommandRead, CommandWrite):
    """
    模拟通道偏置电压配置命令
    """
    def write(self, value: Any) -> str:
        if _digital_arg_check(value):
            return super().write(value)
        raise ValueError(f"Channel offset Invalid value: {value}")


class ChannelCoupling(CommandRead, CommandWrite):
    """
    模拟通道的输入耦合命令
    """
    def write(self, value: Any) -> str:
        if isinstance(value, str) and value.upper() in ("AC", "DC", "GND"):
            return super().write(value)
        raise ValueError(f"Channel Coupling Invalid value: {value}")


class ChannelBWLimit(CommandRead, CommandWrite):
    """
    模拟通道带宽限制命令
    """
    def write(self, value: Any) -> str:
        if isinstance(value, str) and value.upper() in ("20M", "OFF"):
            return super().write(value)
        raise ValueError(f"Channel BW Limit Invalid value: {value}")


class ChannelUnit(CommandRead, CommandWrite):
    """
    模拟通道探头类型命令
    """
    __units_list = ('VOLTage', 'AMPere')

    def write(self, value: Any) -> str:
        if isinstance(value, str):
            value = next((_value for _value in self.__units_list if _value.upper() == value.upper()), None)
            if value is not None:
                return super().write(value)
        raise ValueError(f"Channel Unit Invalid value: {value}")


class ChannelProbe(CommandRead, CommandWrite):
    """
    模拟通道探头衰减比命令
    """
    __dc_attenuation_ratio = (0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000)
    __ac_attenuation_ratio = (10, 5, 2, 1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001)

    def write(self, value: Any) -> str:
        if isinstance(value, float) or isinstance(value, int):
            _value = next((_value for _value in self.__dc_attenuation_ratio if _value == value), None)
            if _value is None:
                _value = next((_value for _value in self.__ac_attenuation_ratio if _value == value), None)
            if _value is not None:
                return super().write(_value)
        raise ValueError(f"Channel Probe Invalid value: {value}")


class ChannelTermination(CommandRead, CommandWrite):
    """
    模拟通道终端电阻命令
    """
    term_dict = {'1M': 1000000, "50": 50}

    def write(self, value: Any) -> str:
        _value = None
        for key, item in self.term_dict.items():
            if isinstance(value, float) or isinstance(value, int):
                _value = key if value == item else None
            if isinstance(value, str):
                _value = key if value.upper() == key else None
            if _value is not None:
                return super().write(_value)
        raise ValueError(f"Channel Termination Invalid value: {value}")


class ChannelInvert(CommandRead, CommandWrite):
    """
    模拟通道输入反向命令
    """
    def write(self, value: Any) -> str:
        if _bool_arg_check(value):
            return super().write(value)
        raise ValueError(f"Channel Invert Invalid value: {value}")


class ChannelDelay(CommandRead, CommandWrite):
    """
    模拟通道延迟校正时间命令
    """
    def write(self, value: Any) -> str:
        if _digital_arg_check(value):
            return super().write(value)
        raise ValueError(f"Channel Delay Invalid value: {value}")
    pass


class ChannelCommand(ValidChannelCheck):
    """
    ZDS系列示波器模拟通道配置命令树构建。

    属性：
        - ``.display``: ``DISPlay`` 命令树；
        - ``.vernier``: ``VERNier`` 命令树；
        - ``.scale``: ``SCALe`` 命令树；
        - ``.offset``: ``OFFSet`` 命令树；
        - ``.coupling``: ``COUPling`` 命令树；
        - ``.bw_limit``: ``BWLimit`` 命令树；
        - ``.units``: ``UNITs`` 命令树；
        - ``.probe``: ``PROBe`` 命令树；
        - ``.termination``: ``TERMination`` 命令树；
        - ``.invert``: ``INVert`` 命令树；
        - ``.delay``: ``DELAy`` 命令树。
    """

    def __init__(self, dev, command_syntax: str = ":CHANnel<n>"):
        # print("ChannelCommand Init")
        super().__init__(dev, command_syntax)
        self._display = ChannelDisplay(dev, f"{self._command_syntax}:DISPlay")
        self._vernier = ChannelVernier(dev, f"{self._command_syntax}:VERNier")
        self._scale = ChannelScale(dev, f"{self._command_syntax}:SCALe")
        self._offset = ChannelOffset(dev, f"{self._command_syntax}:OFFSet")
        self._coupling = ChannelCoupling(dev, f"{self._command_syntax}:COUPling")
        self._bw_limit = ChannelBWLimit(dev, f"{self._command_syntax}:BWLimit")
        self._units = ChannelUnit(dev, f"{self._command_syntax}:UNITs")
        self._probe = ChannelProbe(dev, f"{self._command_syntax}:PROBe")
        self._termination = ChannelTermination(dev, f"{self._command_syntax}:TERMination")
        self._invert = ChannelInvert(dev, f"{self._command_syntax}:INVert")
        self._delay = ChannelDelay(dev, f"{self._command_syntax}:DELAy")

    @property
    def display(self):
        return self._display

    @property
    def vernier(self):
        return self._vernier

    @property
    def scale(self):
        return self._scale

    @property
    def offset(self):
        return self._offset

    @property
    def coupling(self):
        return self._coupling

    @property
    def bw_limit(self):
        return self._bw_limit

    @property
    def units(self):
        return self._units

    @property
    def probe(self):
        return self._probe

    @property
    def termination(self):
        return self._termination

    @property
    def invert(self):
        return self._invert

    @property
    def delay(self):
        return self._delay
