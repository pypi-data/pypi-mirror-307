# import re
# import sys
from typing import *
from functools import total_ordering
from collections import defaultdict


class DefaultDictPassKeyToFactory(defaultdict):
    """
    当访问不存在的键时，将以键为参数访问‘default_factory’工厂函数
    """
    def __init__(self, default_factory: Callable[[Union[int, str]], Any], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.__default_factory = default_factory

    def __missing__(self, key: Any) -> Any:
        if self.__default_factory is not None:
            dict.__setitem__(self, key, self.__default_factory(key))
            return self[key]
        return super().__missing__(key)


@total_ordering
class BaseCommand:

    def __init__(self, dev, command_syntax):
        # print("BaseCommand Init")
        self._command_syntax = command_syntax.rstrip(',')
        self._device = dev

    def __eq__(self, other) -> bool:
        """ 字符串比较是否相等，装饰器’total_ordering‘会自动实现不相等的方法 """
        if not isinstance(other, BaseCommand):
            return NotImplemented
        return str(self) == str(other)

    def __lt__(self, other):
        """ 小于比较 """
        if not isinstance(other, BaseCommand):
            return NotImplemented
        return str(self) < str(other)

    def __hash__(self) -> int:
        return hash(str(self))

    def __str__(self) -> str:
        return self._command_syntax

    @property
    def syntax(self) -> str:
        """ 返回命令字符串 """
        return self._command_syntax

    @property
    def dev(self):
        """ 返回命令对应的设备对象 """
        return self._device


class CommandWriteNoValue(BaseCommand):

    def write(self) -> str:
        self._device.write(self._command_syntax)
        """ 写操作过后读操作，算一次完整的命令执行 """
        """ 2秒可作为写命令后仪器成功执行动作的时间 """
        self._device.read(1024, 2)
        return ""


class CommandWrite(BaseCommand):

    def write(self, value: Any) -> str:
        if value is None:
            raise ValueError("value can not be None")
        if isinstance(value, str):
            value = value.strip("'").strip('"').strip(':')
        if ' ' in self._command_syntax:
            self._device.write(f"{self._command_syntax},{value}")
        else:
            self._device.write(f"{self._command_syntax} {value}")
        """ 写操作过后读操作，算一次完整的命令执行 """
        """ 2秒可作为写命令后仪器成功执行动作的时间 """
        self._device.read(1024, 2)
        return ""


class CommandReadWithValue(BaseCommand):
    def read(self, value: str) -> str:
        if value is None:
            raise ValueError("value can not be None")
        value = value.strip("'").strip('"').strip(':')
        self._device.write(self._command_syntax + f"? {value}".strip())
        return self._device.read(1024, 2).decode("gb2312").rstrip('\r\n\x00')


class CommandRead(BaseCommand):

    def read(self) -> str:
        if ' ' in self._command_syntax:
            self._device.write(self._command_syntax.replace(' ', '? '))
        else:
            self._device.write(self._command_syntax + "?")
        return self._device.read(1024, 2).decode("gb2312").rstrip('\r\n\x00')
