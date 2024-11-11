from commands.command import *


class CLS(CommandWriteNoValue):
    """
    状态清除命令
    """
    def __init__(self, dev, command_syntax: str = "*CLS"):
        super().__init__(dev, command_syntax)
    pass


class ESE(CommandWrite, CommandRead):
    """
    仪器标准事件寄存器使能命令
    """

    def __init__(self, dev, command_syntax: str = "*ESE"):
        super().__init__(dev, command_syntax)


class ESR(CommandRead):
    """
    查询仪器标准事件寄存器状态命令
    """

    def __init__(self, dev, command_syntax: str = "*ESR"):
        super().__init__(dev, command_syntax)


class IDN(CommandRead):
    """
    查询仪器设备信息命令
    """

    def __init__(self, dev, command_syntax: str = "*IDN"):
        super().__init__(dev, command_syntax)


class OPC(CommandWriteNoValue, CommandRead):
    """
    查询仪器设备信息命令
    """

    def __init__(self, dev, command_syntax: str = "*OPC"):
        super().__init__(dev, command_syntax)


class RST(CommandWriteNoValue):
    """
    配置仪器标准事件状态寄存器操作完成位命令
    """

    def __init__(self, dev, command_syntax: str = "*RST"):
        super().__init__(dev, command_syntax)


class SRE(CommandWrite, CommandRead):
    """
    仪器状态字节寄存器组设置使能命令
    """

    def __init__(self, dev, command_syntax: str = "*SRE"):
        super().__init__(dev, command_syntax)


class STB(CommandRead):
    """
    仪器状态字节寄存器组查询命令
    """

    def __init__(self, dev, command_syntax: str = "*STB"):
        super().__init__(dev, command_syntax)


class TST(CommandRead):
    """
    仪器自检结果命令
    """

    def __init__(self, dev, command_syntax: str = "*TST"):
        super().__init__(dev, command_syntax)


class PSC(CommandWrite, CommandRead):
    """
    仪器加电状态清除命令
    """

    def __init__(self, dev, command_syntax: str = "*PSC"):
        super().__init__(dev, command_syntax)

    def write(self, value: int) -> str:
        if value in range(0, 2):
            return super().write(value)
        raise ValueError("Values are only supported in {0|1}")
