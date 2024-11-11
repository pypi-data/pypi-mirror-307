import time
from drivers.multimeter.dmm6000 import DMM6000Device
from drivers.oscillograph.zds.zds5054.zds5054pro import ZDS5054ProDevice
from inst_manager import InstManager


# with InstManager() as inst_manager:
#     # 实例化一个ZDS5054型号的仪器
#     osc: ZDS5054ProDevice = inst_manager.inst_create(instrumentation="ZDS5054PRO", address='192.168.138.13', port=5025)
#
#     # 相当于面控的Clear按键
#     osc.commands.cls.write()
#
#     # 读取仪器系统信息
#     print(osc.commands.idn.read())
#     # 读取仪器制造商、型号、序列号、版本号
#     print(osc.manufacturer)
#     print(osc.model)
#     print(osc.serial)
#     print(osc.version)
#
#     osc.commands.root.stop.write()
#     osc.commands.root.run.write()
#
#     # 读取仪器通道1是否打开 语法：“:CHANnel1:DISPlay?”
#     print((f := osc.commands.ch[1].display.read()))
#
#     # 打开通道2 语法：“:CHANnel2:DISPlay 1”
#     osc.commands.ch[2].display.write(1)
#     # 语法：“:CHANnel2:DISPlay?”
#     print((s := osc.commands.ch[2].display.read()))
#
#     # 关闭通道2 语法：“:CHANnel2:DISPlay 0”
#     osc.commands.ch[2].display.write(0)
#     # 语法：“:CHANnel2:DISPlay?”
#     print((d := osc.commands.ch[2].display.read()))
#
#     # 获取通道1探头类型命令语法
#     print(osc.commands.ch[1].units.syntax)
#     osc.write(osc.commands.ch[1].units.syntax + "?")
#     print((g := osc.read(1024, 2)))
#
#     # 获取通道1探头类型 语法：“:CHANnel1:UNITs?”
#     print((h := osc.commands.ch[1].units.read()))
#
#     # 设置通道1的垂直灵敏度
#     osc.commands.ch[1].scale.write(1.0)
#
#     # 获取通道1的垂直灵敏度
#     print((j := osc.commands.ch[1].scale.read()))
#
#     # 设置通道1的探头的衰减比
#     osc.commands.ch[1].probe.write(0.2)
#     print((k := osc.commands.ch[1].probe.read()))
#     osc.commands.ch[1].probe.write(10)
#     print((l := osc.commands.ch[1].probe.read()))
#
#     # 打开测试峰值(可以不执行)
#     osc.commands.measure.vpp.base.ch[1].write()
#     # 获取测试峰值
#     print(q := osc.commands.measure.vpp.base.ch[1].read())
#     print(w := osc.commands.measure.vpp.state.ch[1].read())
#     print(e := osc.commands.measure.vpp.current.ch[1].read())
#     print(r := osc.commands.measure.vpp.maximum.ch[1].read())
#     print(t := osc.commands.measure.vpp.minimum.ch[1].read())
#     print(y := osc.commands.measure.vpp.average.ch[1].read())
#     print(u := osc.commands.measure.vpp.deviation.ch[1].read())
#     print(i := osc.commands.measure.vpp.count.ch[1].read())
#     # 获取测试峰值的语法
#     print((p := osc.commands.measure.vpp.base.ch[1].syntax))
#
#     # 获取N周期有效值的当前值
#     print(o := osc.commands.measure.vavg.current.cycle.ch[1].read())
#     # 获取全屏周期有效值的当前值
#     print(n := osc.commands.measure.vavg.current.display.ch[1].read())
#     # 获取N/全屏周期有效值的语法
#     print(p := osc.commands.measure.vavg.base.cycle.ch[1].syntax)
#     print(a := osc.commands.measure.vavg.base.display.ch[1].syntax)
#
#     # 获取N周期的比率测量状态、当前值
#     print(s := osc.commands.measure.vratio.state.cycle.ch[1].ch[2].read())
#     print(o := osc.commands.measure.vratio.current.cycle.ch[1].ch[2].read())
#
#     # 获取直流、N周期的状态、当前值
#     print(o := osc.commands.measure.vrms.state.ac.cycle.ch[1].read())
#     print(s := osc.commands.measure.vrms.current.dc.cycle.ch[1].read())
#
#     # 获取上升沿计数测量状态、当前值
#     print(o := osc.commands.measure.rcount.state.ch[1].read())
#     print(s := osc.commands.measure.rcount.current.ch[1].read())
#
#     # 获取通道间的上升沿到上升沿延迟的测量状态、当前值
#     print(o := osc.commands.measure.rrdelay.state.ch[1].ch[2].read())
#     print(s := osc.commands.measure.rrdelay.current.ch[1].ch[2].read())
#
#     # 配置建立保持通道
#     print(q := osc.commands.measure.shold.samp.read())
#     print(w := osc.commands.measure.shold.samp.either.write())
#     print(e := osc.commands.measure.shold.tch.read())
#     print(r := osc.commands.measure.shold.tch.ch[1].write())
#     print(t := osc.commands.measure.shold.dch.read())
#     print(y := osc.commands.measure.shold.dch.ch[2].write())
#
#     # 配置高阈值
#     print(q := osc.commands.measure.threshold.upper.read())
#     print(w := osc.commands.measure.threshold.upper.write(80))
#     print(e := osc.commands.measure.threshold.upper.read())
#     print(r := osc.commands.measure.threshold.upper.write(90))
#
#     # 配置测量范围
#     print(q := osc.commands.measure.scope.read())
#     print(w := osc.commands.measure.scope.zoom1.write())
#     print(e := osc.commands.measure.scope.read())
#     print(r := osc.commands.measure.scope.main.write())
#
#     # 配置触发模式
#     print(a := osc.commands.trigger.mode.edge.write())
#     print(b := osc.commands.trigger.mode.read())
#     print(c := osc.commands.trigger.mode.timeout.write())
#     print(d := osc.commands.trigger.mode.read())
#
#     # 配置超时触发超时时间参数
#     print(e := osc.commands.trigger.timeout.time.write(0.1))
#     print(f := osc.commands.trigger.timeout.time.read())
#     pass


# with InstManager() as inst:
#     dmm:DMM6000Device = inst.inst_create(instrumentation="DMM6001", address='192.168.138.14', port=4999)
#
#     # 读取仪器系统信息
#     print(dmm.commands.idn.read())
#     # 读取仪器制造商、型号、序列号、版本号
#     print(dmm.manufacturer)
#     print(dmm.model)
#     print(dmm.serial)
#     print(dmm.version)
#
#
#     """
#     推荐先使用配置命令配置量程和精度，再使用测量命令进行测量。这样可以有效避免两次测量之间，
#     因参数不同而发生继电器切换，导致仪器测量结果尚未完成的情况。
#     """
#     # 配置并测量直流电压值 使用默认量程
#     dmm.commands.configure.voltage.dc.default.write()
#     print(k := dmm.commands.measure.voltage.dc.default.read())
#
#     # 测量直流电压值 使用默认量程
#     print(k := dmm.commands.measure.voltage.dc.default.read())
#     # 测量直流电压值 使用最小量程、默认精度
#     print(m := dmm.commands.measure.voltage.dc.minimum.default.read())
#     # 测量直流电压值 使用指定量程
#     print(z := dmm.commands.measure.voltage.dc.range(1).read())
#     # 测量直流电压值 使用指定量程、精度
#     print(x := dmm.commands.measure.voltage.dc.range(0.1).maximum.read())
#     # 测量直流电压值 使用指定量程、指定精度
#     print(c := dmm.commands.measure.voltage.dc.range(0.01).resolution(0.001).read())
#     # 测量直流电压值 使用最大量程、指定精度
#     print(v := dmm.commands.measure.voltage.dc.maximum.resolution(0.001).read())
#
#     # 测量电阻值 使用默认量程
#     print(q := dmm.commands.measure.resistance.default.read())
#     # 测量电阻值 使用最小量程、最大精度
#     print(w := dmm.commands.measure.resistance.minimum.maximum.read())
#     # 测量电阻值 使用指定量程
#     print(e := dmm.commands.measure.resistance.range(10000).read())
#     # 测量电阻值 使用指定量程、最小精度
#     print(r := dmm.commands.measure.resistance.range(1000).minimum.read())
#     # 测量电阻值 使用指定量程、指定精度
#     print(t := dmm.commands.measure.resistance.range(100).resolution(0.1).read())
#     # 测量电阻值 使用最大量程、指定精度
#     print(y := dmm.commands.measure.resistance.maximum.resolution(1000).read())
#
#     # 测量频率值 使用默认量程
#     print(w := dmm.commands.measure.frequency.default.read())
#
#     # 测量温度值 使用传感器PT100
#     print(q := dmm.commands.measure.temperature.pt100.read())
#     # 测量温度值 使用传感器PT100、单位为摄氏度
#     print(w := dmm.commands.measure.temperature.pt100.c.read())
#
#     # 配置连通测量并读取数据
#     print(q := dmm.commands.measure.continuity.read())
#
#     # 配置直流电压使用默认量程
#     dmm.commands.configure.voltage.dc.default.write()
#     # 配置直流电压使用最大量程、最大精度
#     dmm.commands.configure.voltage.dc.maximum.maximum.write()
#     # 配置直流电压使用指定量程
#     dmm.commands.configure.voltage.dc.range(1).write()
#     # 配置直流电压使用指定量程、最小精度
#     dmm.commands.configure.voltage.dc.range(0.1).minimum.write()
#     # 配置直流电压使用指定量程、指定精度
#     dmm.commands.configure.voltage.dc.range(0.01).resolution(0.001).write()
#     # 配置直流电压使用最大量程、指定精度
#     dmm.commands.configure.voltage.dc.maximum.resolution(0.001).write()
#
#     print(dmm.write('FUNCtion "VOLTage:DC?"'))
#     print(dmm.read(1024, 2))
#
#     # 配置直流电压的量程参数
#     print(w := dmm.commands.sense.voltage.dc.range.range(1).write())
#     # 配置直流电压的最小量程参数
#     print(e := dmm.commands.sense.voltage.dc.range.minimum.write())
#     # 配置直流电压的最大量程参数
#     print(r := dmm.commands.sense.voltage.dc.range.minimum.read())
#
#     # 配置输入阻抗为自动
#     print(d := dmm.commands.impedance.auto.on.write())
#     pass
