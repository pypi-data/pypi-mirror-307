from commands.ieee_commands import *
from commands.zds.root_commands import *
from commands.zds.ch_commands import *
from commands.zds.measure_commands import *
from commands.zds.trigger_commands import *


class ZDS2024Command:
    """
    ZDS2024系列示波器命令树

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
        - ``.trigger``: ``TRIG`` 命令树。
    """

    def __init__(self, dev):
        # print("ZDS2024Command Init")
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
        self._trigger = TriggerCommand(dev, ":TRIG")

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
