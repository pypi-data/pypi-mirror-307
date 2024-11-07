# CY3761 | fb764bc@outlook.com | 2024-10-27 19:45:23 | __init__.py
# ----------------------------------------------------------------------------------------------------
"""

"""
# ----------------------------------------------------------------------------------------------------
# @overload
# 作为重构函数的修饰器, 效果不理想, 不推荐使用
# 所有相关类型都写在这里, 并设置前缀 T_
# 这里只做值的类型编写, 不做函数类型编写
# ----------------------------------------------------------------------------------------------------
from typing import TypeVar, get_args

# ----------------------------------------------------------------------------------------------------
# TypeVar(name: str,*constraints: Any,...)
# 不允许单个约束 (即不能只传第二参数, 至少传第二参数和第三参数)
# TypeVar 类型变量不能用在 isinstance
# T: 任意类型, 泛型类型
T = TypeVar('T')
T_Number = int | float


# ----------------------------------------------------------------------------------------------------
def main():
    pass


# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()

# 在这里进行导入各模块
# from src.a00.u00 import fn_00
# from src.a00.u01 import fn_01
# from src.a00.u02 import fn_02

# 处理存根
# def handle_stubs():
#     from pathlib import Path
#     from os.path import normpath, sep, getsize
#     from hashlib import md5
#     from shutil import copy
#
#     def storage(name: Path, data=None):
#         read = int(data is None)
#         data = [data, []][read]
#         mode = ['w', 'r'][read] + 't'
#
#         with name.open(mode, encoding='utf-8') as i0:
#             rets = [
#                 lambda: i0.writelines(data),
#                 lambda: i0.readlines(),
#             ][read]()
#
#         return rets
#
#     def refresh_code(name: Path, code: str, size=3):
#         a010 = '\n'
#         data = storage(name) + [a010] * size
#
#         # print(len(data))
#         # [print(repr(v)) for v in data]
#
#         text = '# code: %s%s' % (code, a010)
#
#         # print(data, len(data), text == data[size - 1])
#
#         if text == data[size - 1]:
#             pass
#             # return
#
#         data[size - 1] = text
#
#         while data and data[-1] == a010:
#             data.pop()
#
#         # print(data, len(data))
#
#         return storage(name, data)
#
#     # __name__: 用于标识模块的名称
#     # __package__: 当前模块所属的包的名称. 如果模块没有属于任何包, 值可能是 None
#     # 通常情况下, __name__ 和 __package__ 的值是相同的, 在使用 importlib 动态加载模块 或 使用 runpy 运行模块
#     mod_name = __name__
#     pkg_name = __package__
#
#     if mod_name != pkg_name:
#         return
#
#     # __path__: 存储包的初始化目录绝对路径 (在不被识别为包时, 可能未定义)
#     # 当其他模块导入该包时, Python 会按照 __path__ 变量中定义的路径去查找包内的模块 (默认情况下只有一个元素)
#     # next(iter()) 通过迭代器来访问第一个元素
#     pkg_d_path = next(iter(globals().get('__path__', [])))
#     stu_d_path = Path(pkg_d_path).parent / 'stubs'
#
#     # generator (生成器)
#     # 通过使用 yield 关键字来定义返回值
#     # 调用生成器的 __next__() 方法时, 它会返回一个值并暂停执行, 直到下一次调用 __next__() 方法时再继续执行
#
#     f_suffix_0 = '.py'
#     f_suffix_1 = f_suffix_0 + 'i'
#
#     pkg_f_paths = sorted(Path(pkg_d_path).glob('**/*' + f_suffix_0))
#
#     # f_path: <class 'pathlib.WindowsPath'>
#     for pkg_f_path in pkg_f_paths:
#         pkg_f_path = Path(pkg_f_path)
#         pkg_f_name = pkg_f_path.name.replace(pkg_f_path.suffix, '')  # 不带后缀名
#
#         if pkg_f_name.startswith('_'):
#             continue
#
#         if pkg_f_name.count('.'):
#             continue
#
#         # normpath: 规范化路径, 去除冗余的分隔符和上级目录引用
#         pkg_f_rela = str(normpath(pkg_f_path)).replace(pkg_d_path, '').replace(sep, '/')
#
#         # int(*,base) | base: 进制基数, 表示输入值的进制, 这里是传入一个 16进制字符串, 返回一个10进制数字
#         # md5(''.encode()).hexdigest() | md5, 使用 0~9, a~f | 函数内存入一个 bytes, 返回一个 16进制字符串
#         # 返回的数字长度不确定的, 这里使用 40 位数字
#         stu_f_code = str(int(md5(pkg_f_rela.encode()).hexdigest(), 16)).zfill(40)
#
#         # [print(i, type(v), v) for i, v in enumerate([pkg_f_path, pkg_f_name, pkg_f_rela, stu_f_code])]
#         # print(len(stu_f_code))
#
#         # stubs 目录内 *.pyi 文件路径
#         stu_f_path = stu_d_path / (stu_f_code + f_suffix_1)
#         # print('stu_f_path', stu_f_path)
#
#         # 不存在进行创建, 存在且为空则删除 (创建执行的不执行删除)
#         is_exists = stu_f_path.exists()
#
#         if not is_exists:
#             storage(stu_f_path, [])
#
#         # 复制 pyi 的目标文件路径
#         dst_f_path = pkg_f_path.parent / (pkg_f_name + f_suffix_1)
#
#         # print('dst_f_path', dst_f_path)
#
#         if getsize(stu_f_path):
#             refresh_code(pkg_f_path, stu_f_code)
#
#             copy(stu_f_path, dst_f_path)
#         elif is_exists:
#             stu_f_path.unlink()
#
#
# # handle_stubs()

# 如果内部又有导入 src 的, 则可能会出现异常问题, 或者重复被导入
# 虽然 __init__ 依然重复执行, 使用 main 只执行一次且没有错误
if __name__ == '__main__':
    pass
    # print('__init__.py', fn_00)
    # print('__init__.py', fn_01)
    # print('__init__.py', fn_02)
