from commands.ieee_commands import *
from commands.zds.root_commands import *
from commands.zds.ch_commands import *
from commands.zds.measure_commands import *
from commands.zds.trigger_commands import *


class ZDS5054TriggerATOBnCommand(BaseCommand):
    """
    ZDS5054系列示波器A->Bn触发命令树构建。

    属性：
        - ``.a_src``: ``ASrc`` 命令；
        - ``.b_src``: ``BSrc`` 命令；
        - ``.a_slope``: ``ASlope`` 命令；
        - ``.b_slope``: ``BSlope`` 命令；
        - ``.edge_num``: ``EDGEnum`` 命令；
        - ``.level``: ``LEVel`` 命令。
    """
    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._a_src = TriggerSourceCommand(dev, f"{command_syntax}:ASrc")
        self._b_src = TriggerSourceCommand(dev, f"{command_syntax}:BSrc")
        self._a_slope = TriggerRootSlopeCommand(dev, f"{command_syntax}:ASlope")
        self._b_slope = TriggerRootSlopeCommand(dev, f"{command_syntax}:BSlope")
        self._edge_num = TriggerRWCommand(dev, f"{command_syntax}:EDGEnum", [1, 65535])
        self._level = TriggerSourceRWCommand(dev, f"{command_syntax}:LEVel", None)

    @property
    def a_src(self):
        return self._a_src

    @property
    def b_src(self):
        return self._b_src

    @property
    def a_slope(self):
        return self._a_slope

    @property
    def b_slope(self):
        return self._b_slope

    @property
    def edge_num(self):
        return self._edge_num

    @property
    def level(self):
        return self._level


class ZDS5054TriggerAlterCommand(BaseCommand):
    """
    ZDS5054系列示波器交替触发命令树。

    属性：
        - ``.source``: ``SOURce`` 触发通道命令；
        - ``.level``: ``LEVel`` 参数。
    """

    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._source = TriggerSourceCommand(dev, f"{command_syntax}:SOURce")
        self._level = TriggerSourceRWCommand(dev, f"{command_syntax}:LEVel", None)

    @property
    def source(self):
        return self._source

    @property
    def level(self):
        return self._level


class ZDS5054TriggerModeCommand(TriggerModeCommand):
    """
    ZDS5054系列示波器触发模式命令树构建。

    属性：
        - ``.a_to_b``: ``ATOBn`` 命令；
        - ``.alter``: ``ALTEr`` 参数。
    """

    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._a_to_b = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} ATOBn")
        self._alter = MeasureOnlyWriteNoValueCommand(dev, f"{self._command_syntax} ALTEr")

    @property
    def a_to_b(self):
        return self._a_to_b

    @property
    def alter(self):
        return self._alter


class ZDS5054TriggerCommand(TriggerCommand):
    """
    ZDS5054系列示波器的触发命令树构建。

    属性：
        - ``.mode``: ``MODE`` 命令树；
        - ``.a_to_bn``: ``ATOBn`` 命令树；
        - ``.alter``: ``ALTEr`` 命令树。
    """

    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._mode = ZDS5054TriggerModeCommand(dev, f"{self._command_syntax}:MODE")
        self._a_to_bn = ZDS5054TriggerATOBnCommand(dev, f"{self._command_syntax}:ATOBn")
        self._alter = ZDS5054TriggerAlterCommand(dev, f"{self._command_syntax}:ALTEr")

    @property
    def mode(self):
        return self._mode

    @property
    def a_to_bn(self):
        return self._a_to_bn

    @property
    def alter(self):
        return self._alter


class ZDS5054Command:
    """
    ZDS5054系列示波器命令树

    属性：
        - ``.cls``: ``*CLS`` 命令；
        - ``.ese``: ``*ESE`` 命令；
        - ``.esr``: ``*ESR`` 命令；
        - ``.idn``: ``*IDN`` 命令；
        - ``.opc``: ``*OPC`` 命令；
        - ``.rst``: ``*RST`` 命令；
        - ``.sre``: ``*SRE`` 命令；
        - ``.stb``: ``*STB`` 命令；
        - ``.tst``: ``*TST`` 命令；
        - ``.root``: ``MEASure`` 命令树；
        - ``.ch``: ``CHANnel<n>`` 命令树；
        - ``.measure``: ``MEASure`` 命令树；
        - ``.trigger``: ``TRIG`` 命令树；
        - ``.decode``: ``DECODe:PLUG:EVENt`` 命令。
    """

    def __init__(self, dev):
        # print("ZDS5054Command Init")
        self._cls = CLS(dev)
        self._ese = ESE(dev)
        self._esr = ESR(dev)
        self._idn = IDN(dev)
        self._opc = OPC(dev)
        self._rst = RST(dev)
        self._sre = SRE(dev)
        self._stb = STB(dev)
        self._tst = TST(dev)
        self._root = RootCommand(dev)
        self._ch: Dict[int, ChannelCommand] = DefaultDictPassKeyToFactory(
            lambda n: ChannelCommand(dev, f":CHANnel{n}")
        )
        self._measure = MeasureCommand(dev, ":MEASure")
        self._trigger = ZDS5054TriggerCommand(dev, ":TRIG")
        self._decode = CommandRead(dev, ":DECODe:PLUG:EVENt")

    @property
    def cls(self):
        return self._cls

    @property
    def ese(self):
        return self._ese

    @property
    def esr(self):
        return self._esr

    @property
    def idn(self):
        return self._idn

    @property
    def opc(self):
        return self._opc

    @property
    def rst(self):
        return self._rst

    @property
    def sre(self):
        return self._sre

    @property
    def stb(self):
        return self._stb

    @property
    def tst(self):
        return self._tst

    @property
    def root(self):
        return self._root

    @property
    def ch(self):
        return self._ch

    @property
    def measure(self):
        return self._measure

    @property
    def trigger(self):
        return self._trigger

    @property
    def decode(self):
        return self._decode
