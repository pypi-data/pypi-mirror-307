from commands.command import *



class DMMSenseTypeCommand(BaseCommand):
    """
    询问电流类型命令构建。

    属性：
        - ``.dc``: ``DC`` 命令；
        - ``.ac``: ``AC`` 命令。
    """

    def __init__(self, mixin, cmd_suffix, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._dc: type = mixin(dev, command_syntax + f":DC{cmd_suffix}")
        self._ac: type = mixin(dev, command_syntax + f":AC{cmd_suffix}")

    @property
    def dc(self):
        return self._dc

    @property
    def ac(self):
        return self._ac


class DMMFunctionCommand(BaseCommand):
    """
    查询功能命令参数构建。

    用法：
        - 使用 ``.write()`` 方法，会对仪器发送对应组合命令的写操作。

    属性：
        - ``.voltage``: ``VOLTage`` 命令；
        - ``.current``: ``CURRent`` 命令；
        - ``.resistance``: ``RESistance`` 命令。
        - ``.fresistance``: ``FRESistance`` 命令。
        - ``.capacitance``: ``CAPacitance`` 命令，注：仅支持DMM6000型号。
        - ``.frequency``: ``FREQuency`` 命令。
        - ``.period``: ``PERiod`` 命令，注：仅支持DMM6001型号。
        - ``.temperature``: ``TEMPerature`` 命令。
        - ``.continuity``: ``CONTinuity`` 命令。
        - ``.diode``: ``DIODe`` 命令。
    """

    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._voltage = (
            DMMSenseTypeCommand(CommandWriteNoValue, '"', dev, f'{command_syntax} "VOLTage'))
        self._current = (
            DMMSenseTypeCommand(CommandWriteNoValue, '"', dev, f'{command_syntax} "CURRent'))
        self._resistance = CommandWriteNoValue(dev, f'{command_syntax} "RESistance"')
        self._fresistance = CommandWriteNoValue(dev, f'{command_syntax} "FRESistance"')
        self._capacitance = CommandWriteNoValue(dev, f'{command_syntax} "CAPacitance"')
        self._frequency = CommandWriteNoValue(dev, f'{command_syntax} "FREQuency"')
        self._period = CommandWriteNoValue(dev, f'{command_syntax} "PERiod"')
        self._temperature = CommandWriteNoValue(dev, f'{command_syntax} "TEMPerature"')
        self._continuity = CommandWriteNoValue(dev, f'{command_syntax} "CONTinuity"')
        self._diode = CommandWriteNoValue(dev, f'{command_syntax} "DIODe"')

    @property
    def voltage(self):
        return self._voltage

    @property
    def current(self):
        return self._current

    @property
    def resistance(self):
        return self._resistance

    @property
    def fresistance(self):
        return self._fresistance

    @property
    def capacitance(self):
        if str(self._capacitance.dev.dev_name) == "DMM6000":
            return self._capacitance
        else:
            return f"\033[93m'{self._capacitance.syntax}' {self._capacitance.dev.dev_name} not supported\033[0m"

    @property
    def frequency(self):
        return self._frequency

    @property
    def period(self):
        if str(self._period.dev.dev_name) == "DMM6001":
            return self._period
        else:
            return f"\033[93m'{self._period.syntax}' {self._period.dev.dev_name} not supported\033[0m"

    @property
    def temperature(self):
        return self._temperature

    @property
    def continuity(self):
        return self._continuity

    @property
    def diode(self):
        return self._diode


class DMMSenseWRCommand(CommandWriteNoValue, CommandRead):
    """
    查询可读写命令构建

    用法：
        - 使用 ``.write()`` 方法，会对仪器发送对应组合命令的写操作；
        - 使用 ``.read()`` 方法，会对仪器发送对应的组合命令的读操作并返回相应的字符串结果。
    """

    pass


class DMMSenseMaxMinCommand(BaseCommand):
    """
    查询最大值最小值命令参数构建。

    属性：
        - ``.maximum``: ``MAX`` 参数；
        - ``.minimum``: ``MIN`` 参数。
    """

    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._minimum = DMMSenseWRCommand(dev, f'{command_syntax} MIN')
        self._maximum = DMMSenseWRCommand(dev, f'{command_syntax} MAX')

    @property
    def minimum(self):
        return self._minimum

    @property
    def maximum(self):
        return self._maximum


class DMMAutoCommand(CommandRead):
    """
    查询自动命令参数构建。

    用法：
        - 使用 ``.read()`` 方法，会对仪器发送对应的组合命令的读操作并返回相应的字符串结果。

    属性：
        - ``.off``: ``OFF`` 参数；
        - ``.on``: ``ON`` 参数。
    """
    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._off = CommandWriteNoValue(dev, f'{command_syntax} OFF')
        self._on = CommandWriteNoValue(dev, f'{command_syntax} ON')

    @property
    def off(self):
        return self._off

    @property
    def on(self):
        return self._on


class DMMSenseRangeCommand(DMMSenseMaxMinCommand):
    """
    查询范围命令构建。

    方法：
        - ``.range(<value>)``: ``<range>`` 参数。
    属性：
        - ``.auto``: ``AUTO`` 参数；
    """

    def __init__(self, dev, command_syntax: str = ':RANGe'):
        super().__init__(dev, command_syntax)
        self._auto = DMMAutoCommand(dev, f'{command_syntax}:AUTO')

    def range(self, value: Union[float, int]):
        if not (isinstance(value, float) or isinstance(value, int)):
            raise ValueError("\033[93mOnly float or int type is allowed\033[0m")
        return CommandWriteNoValue(self._device, f'{self._command_syntax} {value}')

    @property
    def auto(self):
        return self._auto


class DMMSenseResolutionCommand(DMMSenseMaxMinCommand):
    """
    查询精度命令构建。

    方法：
        - ``.range(<value>)``: ``<range>`` 参数。
    """

    def __init__(self, dev, command_syntax: str = ':RESolution'):
        super().__init__(dev, command_syntax)

    def resolution(self, value: Union[float, int]):
        if not (isinstance(value, float) or isinstance(value, int)):
            raise ValueError("\033[93mOnly float or int type is allowed\033[0m")
        return CommandWriteNoValue(self._device, f'{self._command_syntax} {value}')


class DMMSenseSetupQueryCommand(BaseCommand):
    """
    查询命令参数构建。

    属性：
        - ``.range``: ``RANGe`` 命令；
        - ``.resolution``: ``RESolution`` 命令。
    """
    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._range = DMMSenseRangeCommand(dev, f'{command_syntax}:RANGe')
        self._resolution = DMMSenseResolutionCommand(dev, f'{command_syntax}:RESolution')

    @property
    def range(self):
        return self._range

    @property
    def resolution(self):
        return self._resolution


class DMMSenseBandwidthCommand(DMMSenseMaxMinCommand):
    """
    查询带宽命令参数构建。

    属性：
        - ``.three``: ``3`` 参数；
        - ``.twenty``: ``20`` 参数；
        - ``.two_hundred``: ``200`` 参数。
    """
    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._3 = CommandWriteNoValue(dev, f'{command_syntax} 3')
        self._20 = CommandWriteNoValue(dev, f'{command_syntax} 20')
        self._200 = CommandWriteNoValue(dev, f'{command_syntax} 200')

    @property
    def three(self):
        return self._3

    @property
    def twenty(self):
        return self._20

    @property
    def two_hundred(self):
        return self._200


class DMMSenseTempDefCommand(CommandRead):
    """
    查询温度命令参数构建。

    用法：
        - 使用 ``.read()`` 方法，会对仪器发送对应的组合命令的读操作并返回相应的字符串结果。

    属性：
        - ``.default``: ``DEF`` 参数；
    """
    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._def = CommandWriteNoValue(dev, f'{command_syntax} DEF')

    @property
    def default(self):
        return self._def


class DMMSenseTempTypeCommand(DMMSenseTempDefCommand):
    """
    查询温度命令传感器类型参数构建。

    属性：
        - ``.pt100``: ``PT100`` 参数；
        - ``.pt200``: ``PT200`` 参数；
        - ``.pt500``: ``PT500`` 参数。
        - ``.pt1000``: ``PT1000`` 参数。
    """
    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._pt100 = CommandWriteNoValue(dev, f'{command_syntax} PT100')
        self._pt200 = CommandWriteNoValue(dev, f'{command_syntax} PT200')
        self._pt500 = CommandWriteNoValue(dev, f'{command_syntax} PT500')
        self._pt1000 = CommandWriteNoValue(dev, f'{command_syntax} PT1000')

    @property
    def pt100(self):
        return self._pt100

    @property
    def pt200(self):
        return self._pt200

    @property
    def pt500(self):
        return self._pt500

    @property
    def pt1000(self):
        return self._pt1000


class DMMSenseTempUnitCommand(DMMSenseTempDefCommand):
    """
    查询温度单位命令参数构建。

    属性：
        - ``.c``: ``C`` 参数；
        - ``.f``: ``F`` 参数；
        - ``.k``: ``K`` 参数。
    """
    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._c = CommandWriteNoValue(dev, f'{command_syntax} C')
        self._f = CommandWriteNoValue(dev, f'{command_syntax} F')
        self._k = CommandWriteNoValue(dev, f'{command_syntax} K')

    @property
    def c(self):
        return self._c

    @property
    def f(self):
        return self._f

    @property
    def k(self):
        return self._k


class DMMSenseTemperatureCommand(BaseCommand):
    """
    查询温度命令构建。

    属性：
        - ``.type``: ``TYPE`` 命令；
        - ``.unit``: ``UNIT`` 命令。
    """
    def __init__(self, dev, command_syntax: str = "TEMPerature"):
        super().__init__(dev, command_syntax)
        self._type = DMMSenseTempTypeCommand(dev, f"{command_syntax}:TYPE")
        self._unit = DMMSenseTempUnitCommand(dev, f"{command_syntax}:UNIT")

    @property
    def type(self):
        return self._type

    @property
    def unit(self):
        return self._unit


class DMMSenseCommand(BaseCommand):
    """
    查询命令构建。

    属性：
        - ``.function``: ``FUNCtion`` 参数树；
        - ``.voltage``: ``VOLTage`` 参数树；
        - ``.current``: ``CURRent`` 参数树。
        - ``.resistance``: ``RESistance`` 参数树；
        - ``.fresistance``: ``FRESistance`` 参数树；
        - ``.capacitance``: ``CAPacitance`` 参数树。
        - ``.frequency``: ``FREQuency`` 参数树；
        - ``.period``: ``PERiod:VOLTage`` 参数树；
        - ``.bandwidth``: ``DETector:BANDwidth`` 参数树。
        - ``.temperature``: ``TEMPerature`` 参数树；
    """
    def __init__(self, dev):
        super().__init__(dev, "SENSe:")
        self._function = DMMFunctionCommand(dev, "FUNCtion")
        self._voltage = DMMSenseTypeCommand(DMMSenseSetupQueryCommand, '', dev, f'VOLTage')
        self._current = DMMSenseTypeCommand(DMMSenseSetupQueryCommand, '', dev, f'CURRent')
        self._resistance = DMMSenseSetupQueryCommand(dev, 'RESistance')
        self._fresistance = DMMSenseSetupQueryCommand(dev, 'FRESistance')
        self._capacitance = DMMSenseRangeCommand(dev, 'CAPacitance')
        self._frequency = DMMSenseRangeCommand(dev, 'FREQuency')
        self._period = DMMSenseRangeCommand(dev, 'PERiod:VOLTage')
        self._bandwidth = DMMSenseBandwidthCommand(dev, 'DETector:BANDwidth')
        self._temperature = DMMSenseTemperatureCommand(dev)

    @property
    def function(self):
        return self._function

    @property
    def voltage(self):
        return self._voltage

    @property
    def current(self):
        return self._current

    @property
    def resistance(self):
        return self._resistance

    @property
    def fresistance(self):
        return self._fresistance

    @property
    def capacitance(self):
        if str(self._capacitance.dev.dev_name) == "DMM6000":
            return self._capacitance
        else:
            return f"\033[93m'{self._capacitance.syntax}' {self._capacitance.dev.dev_name} not supported\033[0m"

    @property
    def frequency(self):
        return self._frequency

    @property
    def period(self):
        if str(self._period.dev.dev_name) == "DMM6001":
            return self._period
        else:
            return f"\033[93m'{self._period.syntax}' {self._period.dev.dev_name} not supported\033[0m"

    @property
    def bandwidth(self):
        return self._bandwidth

    @property
    def temperature(self):
        return self._temperature
