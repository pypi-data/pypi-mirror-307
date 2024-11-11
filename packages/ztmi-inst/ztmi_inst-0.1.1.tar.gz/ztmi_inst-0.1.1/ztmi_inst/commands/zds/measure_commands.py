# ZDS系列测量命令类定义
import re
from commands.zds.ch_commands import ValidChannelCheck
from commands.command import *


class MeasureOnlyWriteNoValueCommand(CommandWriteNoValue):
    pass


class MeasureRWCommand(CommandRead, CommandWrite):
    pass


class MeasureSubCommand(ValidChannelCheck, CommandRead, CommandWriteNoValue):
    """
    双通道命令参数校验，检查是否存在相同通道
    """

    def __init__(self, dev, command_syntax: str, double_channel: bool = False, only_read: bool = False):
        super().__init__(dev, command_syntax)
        if double_channel:
            digital1 = re.compile(r"(\d+)").search(command_syntax)
            digital2 = re.compile(r"(\d+)$").search(command_syntax)
            if (digital1 and digital2) is not None:
                channel1 = int(digital1.group(1))
                channel2 = int(digital2.group(1))
                if channel1 == channel2:
                    raise ValueError(f"Dual channels cannot be the same: {command_syntax}")
        self._only_read = only_read

    def write(self) -> str:
        if self._only_read:
            raise AssertionError(f"'{self._command_syntax}' command read-only")
        return super().write()


class MeasureSholdSampCommand(CommandRead):
    """
    ZDS系列示波器采样类型参数构建。

    属性：
        - ``.positive``: ``POSitive`` 命令；
        - ``.negative``: ``NEGative`` 命令；
        - ``.either``: ``EITHer`` 命令。
    """

    def __init__(self, dev, command_syntax: str = ":SAMP "):
        super().__init__(dev, command_syntax)
        self._positive = CommandWriteNoValue(dev, f"{self._command_syntax}POSitive")
        self._negative = CommandWriteNoValue(dev, f"{self._command_syntax}NEGative")
        self._either = CommandWriteNoValue(dev, f"{self._command_syntax}EITHer")

    @property
    def positive(self):
        return self._positive

    @property
    def negative(self):
        return self._negative

    @property
    def either(self):
        return self._either


class MeasureSholdChannelCommand(CommandRead):
    """
    ZDS系列示波器保持通道参数构建。

    属性：
        - ``.ch``: ``CHANnel<n>`` 参数。
    """

    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._ch: Dict[int, MeasureSubCommand] = DefaultDictPassKeyToFactory(
            lambda n: MeasureSubCommand(dev, f"{command_syntax}CHANnel{n}", False, False)
        )

    @property
    def ch(self):
        return self._ch


class MeasureSholdCommand(BaseCommand):
    """
    ZDS系列示波器保持测量命令树构建。

    属性：
        - ``.tch``: ``TCH`` 命令；
        - ``.dch``: ``DCH`` 命令；
        - ``.samp``: ``SAMP`` 命令。
    """

    def __init__(self, dev, command_syntax: str = ":SHOLd"):
        super().__init__(dev, command_syntax)
        self._tch = MeasureSholdChannelCommand(dev, f"{command_syntax}:TCH ")
        self._dch = MeasureSholdChannelCommand(dev, f"{command_syntax}:DCH ")
        self._samp = MeasureSholdSampCommand(dev, f"{command_syntax}:SAMP ")

    @property
    def tch(self):
        return self._tch

    @property
    def dch(self):
        return self._dch

    @property
    def samp(self):
        return self._samp


class MeasureSingleChannel(ValidChannelCheck):
    """
    ZDS系列示波器单通道命令构建。

    属性：
        - ``.ch``: ``CHANnel<n>`` 参数。
    """

    def __init__(self, dev, command_syntax: str, double_channel: bool = False, only_read: bool = False):
        if double_channel is True:
            super().__init__(dev, command_syntax)
        else:
            super(ValidChannelCheck, self).__init__(dev, command_syntax)
        self._ch: Dict[int, MeasureSubCommand] = DefaultDictPassKeyToFactory(
            lambda n: MeasureSubCommand(dev, f"{command_syntax}CHANnel{n}", double_channel, only_read)
        )

    @property
    def ch(self):
        return self._ch


class MeasureDoubleChannel(BaseCommand):
    """
    ZDS系列示波器双通道参数构建。

    属性：
        - ``.ch``: ``CHANnel<n>`` 参数。
    """

    def __init__(self, dev, command_syntax: str, double_channel: bool = False, only_read: bool = False):
        super().__init__(dev, command_syntax)
        self._ch: Dict[int, MeasureSingleChannel] = DefaultDictPassKeyToFactory(
            lambda n: MeasureSingleChannel(dev, f"{command_syntax}CHANnel{n},", double_channel, only_read)
        )

    @property
    def ch(self):
        return self._ch


class MeasureInterval(BaseCommand):
    """
    ZDS系列示波器测量范围参数构建。

    属性：
        - ``.display``: ``DISPlay`` 参数；
        - ``.cycle``: ``CYCLe`` 参数。
    """

    def __init__(self, dev, command_syntax: str, double_channel: bool = False, only_read: bool = False):
        super().__init__(dev, command_syntax)
        if double_channel:
            _class = MeasureDoubleChannel
        else:
            _class = MeasureSingleChannel

        self._display = _class(dev, f"{command_syntax}DISPlay,", double_channel, only_read)
        self._cycle = _class(dev, f"{command_syntax}CYCLe,", double_channel, only_read)

    @property
    def display(self):
        return self._display

    @property
    def cycle(self):
        return self._cycle


class MeasureCouple(BaseCommand):
    """
    ZDS系列示波器电流类型参数构建。

    属性：
        - ``.ac``: ``AC`` 参数；
        - ``.dc``: ``DC`` 参数。
    """

    def __init__(self, dev, command_syntax: str, double_channel: bool = False, only_read: bool = False):
        super().__init__(dev, command_syntax)
        self._ac = MeasureInterval(dev, f"{command_syntax}AC,", double_channel, only_read)
        self._dc = MeasureInterval(dev, f"{command_syntax}DC,", double_channel, only_read)

    @property
    def ac(self):
        return self._ac

    @property
    def dc(self):
        return self._dc


class MeasureEightCommand(BaseCommand):
    """
    ZDS系列示波器测量命令构建。

    属性：
        - ``.base``: ``None`` 命令；
        - ``.state``: ``STATe`` 命令；
        - ``.current``: ``CURRent`` 命令；
        - ``.maximum``: ``MAXImum`` 命令；
        - ``.minimum``: ``MINImum`` 命令；
        - ``.average``: ``AVERage`` 命令；
        - ``.deviation``: ``DEViation`` 命令；
        - ``.count``: ``COUNt`` 命令。
    """

    def __init__(
        self,
        dev,
        command_syntax: str,
        couple: bool = False,
        interval: bool = False,
        double_channel: bool = False
    ):
        super().__init__(dev, command_syntax)
        if couple:
            _class = MeasureCouple
        elif interval:
            _class = MeasureInterval
        elif double_channel:
            _class = MeasureDoubleChannel
        else:
            _class = MeasureSingleChannel
        self._base = _class(dev, f"{command_syntax} ", double_channel, False)
        self._state = _class(dev, f"{command_syntax}:STATe ", double_channel, True)
        self._current = _class(dev, f"{command_syntax}:CURRent ", double_channel, True)
        self._maximum = _class(dev, f"{command_syntax}:MAXImum ", double_channel, True)
        self._minimum = _class(dev, f"{command_syntax}:MINImum ", double_channel, True)
        self._average = _class(dev, f"{command_syntax}:AVERage ", double_channel, True)
        self._deviation = _class(dev, f"{command_syntax}:DEViation ", double_channel, True)
        self._count = _class(dev, f"{command_syntax}:COUNt ", double_channel, True)

    @property
    def base(self):
        return self._base

    @property
    def state(self):
        return self._state

    @property
    def current(self):
        return self._current

    @property
    def maximum(self):
        return self._maximum

    @property
    def minimum(self):
        return self._minimum

    @property
    def average(self):
        return self._average

    @property
    def deviation(self):
        return self._deviation

    @property
    def count(self):
        return self._count


class MeasureScopeCommand(CommandRead):
    """
    ZDS系列示波器测量范围命令树构建。

    属性：
        - ``.main``: ``MAIN`` 命令；
        - ``.zoom1``: ``ZOOM1`` 命令；
        - ``.zoom2``: ``ZOOM2`` 命令；
        - ``.cursor``: ``CURSor`` 命令。
    """

    def __init__(self, dev, command_syntax: str = ":SCOPe"):
        super().__init__(dev, command_syntax)
        self._main = MeasureOnlyWriteNoValueCommand(dev, f"{self._command_syntax} MAIN")
        self._zoom1 = MeasureOnlyWriteNoValueCommand(dev, f"{self._command_syntax} ZOOM1")
        self._zoom2 = MeasureOnlyWriteNoValueCommand(dev, f"{self._command_syntax} ZOOM2")
        self._cursor = MeasureOnlyWriteNoValueCommand(dev, f"{self._command_syntax} CURSor")

    @property
    def main(self):
        return self._main

    @property
    def zoom1(self):
        return self._zoom1

    @property
    def zoom2(self):
        return self._zoom2

    @property
    def cursor(self):
        return self._cursor


class MeasureThreshold(BaseCommand):
    """
    ZDS系列示波器测量阈值命令树构建。

    属性：
        - ``.lower``: ``LOWer`` 命令；
        - ``.middle``: ``MIDdle`` 命令；
        - ``.upper``: ``UPper`` 命令。
    """

    def __init__(self, dev, command_syntax):
        super().__init__(dev, command_syntax)
        self._lower = MeasureRWCommand(dev, f"{command_syntax} LOWer")
        self._middle = MeasureRWCommand(dev, f"{command_syntax} MIDdle")
        self._upper = MeasureRWCommand(dev, f"{command_syntax} UPper")

    @property
    def lower(self):
        return self._lower

    @property
    def middle(self):
        return self._middle

    @property
    def upper(self):
        return self._upper


class MeasurePULSetrainCommand(MeasureEightCommand):
    """
    ZDS系列示波器脉冲串命令树构建。

    属性：
        - ``.pset``: ``PSET`` 命令。
    """

    def __init__(self, dev, command_syntax: str = ":PULSetrain"):
        super().__init__(dev, command_syntax)
        self._pset = MeasureRWCommand(dev, f"{command_syntax}:PSET")

    @property
    def pset(self):
        return self._pset


class MeasureCommand(BaseCommand):
    """
    ZDS系列示波器测量命令树构建。

    属性：
        - ``.clear``: ``CLEar`` 命令树；
        - ``.threshold``: ``THResholds`` 命令树；
        - ``.scope``: ``SCOPe`` 命令树；
        - ``.vpp``: ``VPP`` 命令树；
        - ``.vamp``: ``VAMP`` 命令树；
        - ``.vmax``: ``VMAX`` 命令树；
        - ``.vmin``: ``VMIN`` 命令树；
        - ``.vtop``: ``VTOP`` 命令树；
        - ``.vbase``: ``VBASe`` 命令树；
        - ``.rovershoot``: ``ROVErshoot`` 命令树；
        - ``.fovershoot``: ``FOVErshoot`` 命令树；
        - ``.rpreshoot``: ``RPREshoot`` 命令树；
        - ``.fpreshoot``: ``FPREshoot`` 命令树；
        - ``.vavg``: ``VAVG`` 命令树；
        - ``.vrms``: ``VRMS`` 命令树；
        - ``.vratio``: ``VRATio`` 命令树；
        - ``.vmean``: ``VMEAn`` 命令树；
        - ``.period``: ``PERiod`` 命令树；
        - ``.frequency``: ``FREQuency`` 命令树；
        - ``.risetime``: ``RISetime`` 命令树；
        - ``.falltime``: ``FALLtime`` 命令树；
        - ``.pwidth``: ``PWIDth`` 命令树；
        - ``.nwidth``: ``NWIDth`` 命令树；
        - ``.pduty``: ``PDUTy`` 命令树；
        - ``.nduty``: ``NDUTy`` 命令树；
        - ``.bwidth``: ``BWIDth`` 命令树；
        - ``.pulsetrain``: ``PULSetrain`` 命令树；
        - ``.xmax``: ``XAMX`` 命令树；
        - ``.xmin``: ``XMIN`` 命令树；
        - ``.rrdelay``: ``RRDelay`` 命令树；
        - ``.ffdelay``: ``FFDelay`` 命令树；
        - ``.rfdelay``: ``RFDelay`` 命令树；
        - ``.frdelay``: ``FRDelay`` 命令树；
        - ``.rphase``: ``RPHase`` 命令树；
        - ``.fphase``: ``FPHase`` 命令树；
        - ``.shold``: ``SHOLd`` 命令树；
        - ``.setuptime``: ``SETUptime`` 命令树；
        - ``.holdtime``: ``HOLDtime`` 命令树；
        - ``.shratio``: ``SHRAtio`` 命令树；
        - ``.baud``: ``BAUD`` 命令树；
        - ``.rcount``: ``RCOUnt`` 命令树；
        - ``.fcount``: ``FCOUnt`` 命令树；
        - ``.pcount``: ``PCOUnt`` 命令树；
        - ``.ncount``: ``NCOUnt`` 命令树；
        - ``.tcount``: ``TCOUnt`` 命令树；
        - ``.area``: ``AREA`` 命令树；
        - ``.parea``: ``PAREe`` 命令树；
        - ``.narea``: ``NAREa`` 命令树。
    """

    def __init__(self, dev, command_syntax: str = ":MEASure"):
        # print("MeasureCommand Init")
        super().__init__(dev, command_syntax)
        self._clear = MeasureOnlyWriteNoValueCommand(dev, f"{command_syntax}:CLEar")
        self._threshold = MeasureThreshold(dev, f"{command_syntax}:THResholds")
        self._scope = MeasureScopeCommand(dev, f"{command_syntax}:SCOPe")
        self._vpp = MeasureEightCommand(dev, f"{command_syntax}:VPP")
        self._vamp = MeasureEightCommand(dev, f"{command_syntax}:VAMP")
        self._vmax = MeasureEightCommand(dev, f"{command_syntax}:VMAX")
        self._vmin = MeasureEightCommand(dev, f"{command_syntax}:VMIN")
        self._vtop = MeasureEightCommand(dev, f"{command_syntax}:VTOP")
        self._vbase = MeasureEightCommand(dev, f"{command_syntax}:VBASe")
        self._rovershoot = MeasureEightCommand(dev, f"{command_syntax}:ROVErshoot")
        self._fovershoot = MeasureEightCommand(dev, f"{command_syntax}:FOVErshoot")
        self._rpreshoot = MeasureEightCommand(dev, f"{command_syntax}:RPREshoot")
        self._fpreshoot = MeasureEightCommand(dev, f"{command_syntax}:FPREshoot")
        self._vavg = MeasureEightCommand(
            dev, f"{command_syntax}:VAVG", interval=True)
        self._vrms = MeasureEightCommand(
            dev, f"{command_syntax}:VRMS", couple=True, interval=True)
        self._vratio = MeasureEightCommand(
            dev, f"{command_syntax}:VRATio", interval=True, double_channel=True)
        self._vmean = MeasureEightCommand(dev, f"{command_syntax}:VMEAn")
        self._period = MeasureEightCommand(dev, f"{command_syntax}:PERiod")
        self._frequency = MeasureEightCommand(dev, f"{command_syntax}:FREQuency")
        self._risetime = MeasureEightCommand(dev, f"{command_syntax}:RISetime")
        self._falltime = MeasureEightCommand(dev, f"{command_syntax}:FALLtime")
        self._pwidth = MeasureEightCommand(dev, f"{command_syntax}:PWIDth")
        self._nwidth = MeasureEightCommand(dev, f"{command_syntax}:NWIDth")
        self._pduty = MeasureEightCommand(dev, f"{command_syntax}:PDUTy")
        self._nduty = MeasureEightCommand(dev, f"{command_syntax}:NDUTy")
        self._bwidth = MeasureEightCommand(dev, f"{command_syntax}:BWIDth")
        self._pulsetrain = MeasurePULSetrainCommand(dev, f"{command_syntax}:PULSetrain")
        self._xmax = MeasureEightCommand(dev, f"{command_syntax}:XAMX")
        self._xmin = MeasureEightCommand(dev, f"{command_syntax}:XMIN")
        self._rrdelay = MeasureEightCommand(
            dev, f"{command_syntax}:RRDelay", double_channel=True)
        self._ffdelay = MeasureEightCommand(
            dev, f"{command_syntax}:FFDelay", double_channel=True)
        self._rfdelay = MeasureEightCommand(
            dev, f"{command_syntax}:RFDelay", double_channel=True)
        self._frdelay = MeasureEightCommand(
            dev, f"{command_syntax}:FRDelay", double_channel=True)
        self._rphase = MeasureEightCommand(
            dev, f"{command_syntax}:RPHase", double_channel=True)
        self._fphase = MeasureEightCommand(
            dev, f"{command_syntax}:FPHase", double_channel=True)
        self._shold = MeasureSholdCommand(dev, f"{command_syntax}:SHOLd")
        self._setuptime = MeasureEightCommand(dev, f"{command_syntax}:SETUptime")
        self._holdtime = MeasureEightCommand(dev, f"{command_syntax}:HOLDtime")
        self._shratio = MeasureEightCommand(dev, f"{command_syntax}:SHRAtio")
        self._baud = MeasureEightCommand(dev, f"{command_syntax}:BAUD")
        self._rcount = MeasureEightCommand(dev, f"{command_syntax}:RCOUnt")
        self._fcount = MeasureEightCommand(dev, f"{command_syntax}:FCOUnt")
        self._pcount = MeasureEightCommand(dev, f"{command_syntax}:PCOUnt")
        self._ncount = MeasureEightCommand(dev, f"{command_syntax}:NCOUnt")
        self._tcount = MeasureEightCommand(dev, f"{command_syntax}:TCOUnt")
        self._area = MeasureEightCommand(
            dev, f"{command_syntax}:AREA", interval=True)
        self._parea = MeasureEightCommand(
            dev, f"{command_syntax}:PAREe", interval=True)
        self._narea = MeasureEightCommand(
            dev, f"{command_syntax}:NAREa", interval=True)

    @property
    # @abstractmethod
    def clear(self):
        return self._clear

    @property
    def threshold(self):
        return self._threshold

    @property
    def scope(self):
        return self._scope

    @property
    # @abstractmethod
    def vpp(self):
        return self._vpp

    @property
    def vamp(self):
        return self._vamp

    @property
    def vmax(self):
        return self._vmax

    @property
    def vmin(self):
        return self._vmin

    @property
    def vtop(self):
        return self._vtop

    @property
    def vbase(self):
        return self._vbase

    @property
    def rovershoot(self):
        return self._rovershoot

    @property
    def fovershoot(self):
        return self._fovershoot

    @property
    def rpreshoot(self):
        return self._rpreshoot

    @property
    def fpreshoot(self):
        return self._fpreshoot

    @property
    def vavg(self):
        return self._vavg

    @property
    def vrms(self):
        return self._vrms

    @property
    def vratio(self):
        return self._vratio

    @property
    def vmean(self):
        return self._vmean

    @property
    def period(self):
        return self._period

    @property
    def frequency(self):
        return self._frequency

    @property
    def risetime(self):
        return self._risetime

    @property
    def falltime(self):
        return self._falltime

    @property
    def pwidth(self):
        return self._pwidth

    @property
    def nwidth(self):
        return self._nwidth

    @property
    def pduty(self):
        return self._pduty

    @property
    def nduty(self):
        return self._nduty

    @property
    def bwidth(self):
        return self._bwidth

    @property
    def pulsetrain(self):
        return self._pulsetrain

    @property
    # @abstractmethod
    def xmax(self):
        return self._xmax

    @property
    def xmin(self):
        return self._xmin

    @property
    def rrdelay(self):
        return self._rrdelay

    @property
    def ffdelay(self):
        return self._ffdelay

    @property
    def rfdelay(self):
        return self._rfdelay

    @property
    def frdelay(self):
        return self._frdelay

    @property
    def rphase(self):
        return self._rphase

    @property
    def fphase(self):
        return self._fphase

    @property
    def shold(self):
        return self._shold

    @property
    def setuptime(self):
        return self._setuptime

    @property
    def holdtime(self):
        return self._holdtime

    @property
    def shratio(self):
        return self._shratio

    @property
    def baud(self):
        return self._baud

    @property
    def rcount(self):
        return self._rcount

    @property
    def fcount(self):
        return self._fcount

    @property
    def pcount(self):
        return self._pcount

    @property
    def ncount(self):
        return self._ncount

    @property
    def tcount(self):
        return self._tcount

    @property
    def area(self):
        return self._area

    @property
    def parea(self):
        return self._parea

    @property
    def narea(self):
        return self._narea
