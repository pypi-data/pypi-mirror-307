# CY3761 | fb764bc@outlook.com | 2024-10-30 12:14:39 | op.py
# ----------------------------------------------------------------------------------------------------
""""""
from CY3761 import *


# ----------------------------------------------------------------------------------------------------
# 当前函数类型处理办法
# 每次运行当前模块时, 判断 pyi 文件是否存在, 不存在则创建, 该处理执行写在 __init__ 内
# 每个需要创建 pyi的都需要进行导入 from CY3761 import *

# 注意!
# H:\Miniconda\envs\CY3761-src\Lib\typing.py
# C:\Users\CY3761\AppData\Local\Programs\PyCharm Professional\plugins\python-ce\helpers\typeshed\stdlib\typing.pyi
# 这两个文件是可以做的所需功能 (py 与 pyi 不同目录可进行关联类型)
# Has stub item in typing.pyi | py, 在 typing.pyi 中有 stub 项
# Stub for item in typing.py | pyi, typing.py 中项目的存根
# ----------------------------------------------------------------------------------------------------
def add(*args):
    """
    这是一个累加处理的函数.
    需要累加的数值传入到参数 *args 上.
    累加只支持值的数据类型是 int 或 float.
    """
    return sum([v for v in args if isinstance(v, get_args(T_Number))])


# ----------------------------------------------------------------------------------------------------
def main():
    print(add())
    print(add(1, 2))
    print(add(1, 1.1, 2.1, 3.2))


# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
