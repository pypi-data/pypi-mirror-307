from drivers.driver import *
from drivers.inst_device_mapping import INST_DRIVER_MAPPING_GROUP


def single(_class):
    """
    用于实现单例模式装饰器函数
    """
    instances = {}
    # 备份原有的 __new__ 方法
    original_new = _class.__new__

    def new(_class):
        if _class not in instances:
            instances[_class] = original_new(_class)
        return instances[_class]

    _class.__new__ = staticmethod(new)
    return _class


# 仪器管理类（Instrument Manager）
@single
class InstManager:
    def __init__(self):
        self.__created = False
        self.__inst_device = dict()
        pass

    def __enter__(self) -> Self:
        if not self.__created:
            self.inst_open_all()
        return self

    def __del__(self):
        if self.__created:
            self.inst_close_all()
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__created:
            self.inst_close_all()
        pass

    def inst_create(
        self,
        *,
        instrumentation: str = None,
        address: str = "192.168.138.13",
        port: Optional[int] = 5025
    ):

        if instrumentation is None:
            print("The instrumentation cannot be empty")
            return None

        inst_driver = INST_DRIVER_MAPPING_GROUP

        inst_device_class = inst_driver[str(instrumentation)]
        new_inst: Driver = inst_device_class(address, port)
        if new_inst is not None:
            new_inst._dev_number = new_inst.dev_number + 1
            self.__inst_device[instrumentation] = new_inst
            return new_inst
        return None

    def inst_remove(self, inst: Driver = None) -> None:
        if inst is None:
            self.inst_close_all()

        for key in list(self.__inst_device):
            if inst == self.__inst_device[key]:
                inst._dev_number = inst.dev_number - 1
                inst._dev_name = None
                self.__inst_device[key].close()
                del self.__inst_device[key]

    def inst_open_all(self) -> bool:
        for key in list(self.__inst_device):
            self.__inst_device[key].open()
        self.__created = True
        return True

    def inst_close_all(self) -> bool:
        for key in list(self.__inst_device):
            self.__inst_device[key].close()
            self.inst_remove(self.__inst_device[key])
        self.__created = False
        return True

    @property
    def is_created(self) -> bool:
        """ 表示设备管理类是否已经实例化 """
        return self.__created
