from commands.command import *


def create_class(mixin):
    """
    测量命令组和配置命令组在树形结构上相同，前者命令组仅支持查询，后者命令组可读写。
    """

    class DMMResolutionValue(mixin):
        """
        精度命令参数构建。

        用法：
            - 使用 ``.write()`` 方法，会对仪器发送对应组合命令的写操作，如果组合命令不支持写，
            会触发 ``AttributeError`` 错误；
            - 使用 ``.read()`` 方法，会对仪器发送对应的组合命令的读操作并返回相应的字符串结果，
            如果组合命令不支持读，会触发 ``AttributeError`` 错误。

        方法：
            - ``.resolution(<value>)``: ``<resolution>`` 参数。
        属性：
            - ``.default``: ``DEF`` 参数；
            - ``.maximum``: ``MAX`` 参数；
            - ``.minimum``: ``MIN`` 参数。
        """

        def __init__(self, dev, command_syntax: str):
            super().__init__(dev, command_syntax)
            self._default: mixin = mixin(dev, f"{self._command_syntax},DEF")
            self._maximum: mixin = mixin(dev, f"{self._command_syntax},MAX")
            self._minimum: mixin = mixin(dev, f"{self._command_syntax},MIN")

        def resolution(self, value: Union[float, int]) -> mixin:
            if not (isinstance(value, float) or isinstance(value, int)):
                raise ValueError("\033[93mOnly float or int type is allowed\033[0m")
            return mixin(self._device, f"{self._command_syntax},{value}")

        @property
        def default(self) -> mixin:
            return self._default

        @property
        def maximum(self) -> mixin:
            return self._maximum

        @property
        def minimum(self) -> mixin:
            return self._minimum

    class DMMRangeValue(mixin):
        """
        范围命令参数构建。

        用法：
            - 使用 ``.write()`` 方法，会对仪器发送对应组合命令的写操作，如果组合命令不支持写，
            会触发 ``AttributeError`` 错误；
            - 使用 ``.read()`` 方法，会对仪器发送对应的组合命令的读操作并返回相应的字符串结果，
            如果组合命令不支持读，会触发 ``AttributeError`` 错误。

        方法：
            - ``.range(<value>)``: ``<range>`` 参数。
        属性：
            - ``.default``: ``DEF`` 参数；
            - ``.maximum``: ``MAX`` 参数；
            - ``.minimum``: ``MIN`` 参数。
        """

        def __init__(self, dev, command_syntax: str):
            super().__init__(dev, command_syntax)
            self._default = DMMResolutionValue(dev, f"{self._command_syntax} DEF")
            self._maximum = DMMResolutionValue(dev, f"{self._command_syntax} MAX")
            self._minimum = DMMResolutionValue(dev, f"{self._command_syntax} MIN")

        def range(self, value: Union[float, int]):
            if not (isinstance(value, float) or isinstance(value, int)):
                raise ValueError("\033[93mOnly float or int type is allowed\033[0m")
            return DMMResolutionValue(self._device, f"{self._command_syntax} {value}")

        @property
        def default(self):
            return self._default

        @property
        def maximum(self):
            return self._maximum

        @property
        def minimum(self):
            return self._minimum

    class DMMRangeValueNoResolution(mixin):
        """
        范围命令参数构建，不支持精度参数配置。

        用法：
            - 使用 ``.write()`` 方法，会对仪器发送对应组合命令的写操作，如果组合命令不支持写，
            会触发 ``AttributeError`` 错误；
            - 使用 ``.read()`` 方法，会对仪器发送对应的组合命令的读操作并返回相应的字符串结果，
            如果组合命令不支持读，会触发 ``AttributeError`` 错误。

        方法：
            - ``.range(<value>)``: ``<range>`` 参数。
        属性：
            - ``.default``: ``DEF`` 参数；
            - ``.maximum``: ``MAX`` 参数；
            - ``.minimum``: ``MIN`` 参数。
        """

        def __init__(self, dev, command_syntax: str):
            super().__init__(dev, command_syntax)
            self._default = mixin(dev, f"{self._command_syntax} DEF")
            self._maximum = mixin(dev, f"{self._command_syntax} MAX")
            self._minimum = mixin(dev, f"{self._command_syntax} MIN")

        def range(self, value: Union[float, int]):
            if not (isinstance(value, float) or isinstance(value, int)):
                raise ValueError("\033[93mOnly float or int type is allowed\033[0m")
            return mixin(self._device, f"{self._command_syntax} {value}")

        @property
        def default(self):
            return self._default

        @property
        def maximum(self):
            return self._maximum

        @property
        def minimum(self):
            return self._minimum

    class DMMTypeCommand(BaseCommand):
        """
        电流类型命令构建。

        属性：
            - ``.dc``: ``DC`` 命令；
            - ``.ac``: ``AC`` 命令。
        """

        def __init__(self, dev, command_syntax: str):
            super().__init__(dev, command_syntax)
            self._dc = DMMRangeValue(dev, f"{command_syntax}:DC")
            self._ac = DMMRangeValue(dev, f"{command_syntax}:AC")

        @property
        def dc(self):
            return self._dc

        @property
        def ac(self):
            return self._ac

    class DMMTemperatureUnitValue(mixin):
        """
        温度测量单位命令参数构建。

        属性：
            - ``.default``: ``DEF`` 参数；
            - ``.c``: ``C`` 参数；
            - ``.f``: ``F`` 参数；
            - ``.k``: ``K`` 参数；
        """

        def __init__(self, dev, command_syntax: str):
            super().__init__(dev, command_syntax)
            self._default = CommandRead(dev, f"{self._command_syntax},DEF")
            self._c = mixin(dev, f"{self._command_syntax},C")
            self._f = mixin(dev, f"{self._command_syntax},F")
            self._k = mixin(dev, f"{self._command_syntax},K")

        @property
        def default(self):
            return self._default

        # 摄氏度
        @property
        def c(self):
            return self._c

        # 华氏温度
        @property
        def f(self):
            return self._f

        # 开尔文温度
        @property
        def k(self):
            return self._k

    class DMMTemperatureCommand(mixin):
        """
        温度测量传感器类型参数构建。

        属性：
            - ``.default``: ``DEF`` 参数；
            - ``.pt100``: ``PT100`` 参数；
            - ``.pt200``: ``PT200`` 参数；
            - ``.pt500``: ``PT500`` 参数；
            - ``.pt800``: ``PT800`` 参数；
            - ``.pt1000``: ``PT1000`` 参数。
        """

        def __init__(self, dev, command_syntax: str):
            super().__init__(dev, command_syntax)
            self._default = DMMTemperatureUnitValue(dev, f"{self._command_syntax} DEF")
            self._pt100 = DMMTemperatureUnitValue(dev, f"{self._command_syntax} PT100")
            self._pt200 = DMMTemperatureUnitValue(dev, f"{self._command_syntax} PT200")
            self._pt500 = DMMTemperatureUnitValue(dev, f"{self._command_syntax} PT500")
            self._pt800 = DMMTemperatureUnitValue(dev, f"{self._command_syntax} PT800")
            self._pt1000 = DMMTemperatureUnitValue(dev, f"{self._command_syntax} PT1000")

        @property
        def default(self):
            return self._default

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
        def pt800(self):
            return self._pt800

        @property
        def pt1000(self):
            return self._pt1000

    class DMMMeasureConfigCommand(BaseCommand):
        """
        测量、配置命令构建

        属性：
            - ``.voltage``: ``VOLTage`` 命令；
            - ``.current``: ``CURRent`` 命令；
            - ``.resistance``: ``RESistance`` 命令；
            - ``.capacitance``: ``CAPacitance`` 命令，注：仅支持DMM6000型号；
            - ``.frequency``: ``FREQuency`` 命令；
            - ``.period``: ``PERiod`` 命令，注：仅支持DMM6001型号；
            - ``.temperature``: ``TEMPerature`` 命令；
            - ``.continuity``: ``CONTinuity`` 命令；
            - ``.diode``: ``DIODe`` 命令。
        """

        def __init__(self, dev, command_syntax: str):
            super().__init__(dev, command_syntax)
            self._voltage = DMMTypeCommand(dev, f"{command_syntax}:VOLTage")
            self._current = DMMTypeCommand(dev, f"{command_syntax}:CURRent")
            self._resistance = DMMRangeValue(dev, f"{command_syntax}:RESistance")
            self._capacitance = DMMRangeValueNoResolution(dev, f"{command_syntax}:CAPacitance")
            self._frequency = DMMRangeValueNoResolution(dev, f"{command_syntax}:FREQuency")
            self._period = DMMRangeValueNoResolution(dev, f"{command_syntax}:PERiod")
            self._temperature = DMMTemperatureCommand(dev, f"{command_syntax}:TEMPerature")
            self._continuity = mixin(dev, f"{command_syntax}:CONTinuity")
            self._diode = mixin(dev, f"{command_syntax}:DIODe")

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

    return DMMMeasureConfigCommand
