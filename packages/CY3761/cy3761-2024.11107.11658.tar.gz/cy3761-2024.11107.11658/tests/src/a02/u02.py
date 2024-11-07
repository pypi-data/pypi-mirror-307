# https://docs.python.org/zh-cn/3.11/library/typing.html#typing
# 本模块提供对类型提示的运行时支持. 对于类型系统的原始说明, 请参阅 PEP 484. 一个更简明的介绍是 PEP 483

def fn_00(v00: str) -> str:
    return 'Hello %s' % v00


# fn_00 函数中, 参数 v00 的类型应是 str, 返回类型是 str. 子类型也可以作为参数
