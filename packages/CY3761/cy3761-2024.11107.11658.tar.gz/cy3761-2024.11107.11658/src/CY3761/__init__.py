from pathlib import Path
from shutil import copy
from CY3761.__type__ import *


# ----------------------------------------------------------------------------------------------------
class __:
    # 导入模块执行的函数名称
    a_exec = ['__01', '__02']  # '__00',

    # 当前模块执行的函数名称
    b_exec = []

    #  模块的名称
    mod_name = __name__

    # 当前模块所属的包的名称. 如果模块没有属于任何包, 值可能是 None
    pkg_name = __package__

    suffixes = ['.py']

    root = Path(__file__).parent

    encoding = 'utf-8'

    mods: list[list[Path | str]] = []

    a010 = '\n'


__.suffixes.append(__.suffixes[0] + 'i')
__.suffix_0, __.suffix_1 = __.suffixes

__.stub = __.root.parent.parent / 'stub'


def __exec(data: list[str]):
    [
        v() for k, v in globals().items()
        if k in data and k.startswith('__') and k[2:].isdecimal() and callable(v)
    ]


def __storage(name: Path, data=None):
    read = int(data is None)
    data = [data, []][read]
    mode = ['w', 'r'][read] + 't'

    with name.open(mode, encoding=__.encoding) as i0:
        rets = [
            lambda: i0.writelines(['{0}{1}'.format(v, __.a010) for v in data]),
            lambda: i0.readlines(),
        ][read]()

    return rets


# ----------------------------------------------------------------------------------------------------
# 测试环境
def __00():
    from datetime import datetime

    print(datetime.now().isoformat())

    print(__.mod_name, __.pkg_name)
    print()


# 获取当前所有模块
# 过滤文件名下划线开头
# 过滤文件名带 .
def __01():
    for f_path in sorted(__.root.glob('**/*{0}'.format(__.suffix_0))):
        f_path = Path(f_path)
        f_name = f_path.name.replace(f_path.suffix, '')

        if f_name.startswith('_'):
            continue

        if f_name.count('.'):
            continue

        # print(f_path)

        d_rela = f_path.relative_to(__.root)

        __.mods.append([f_path, f_name, d_rela])


# 创建 pyi 文件 (相同目录)
# 发布后未必会有 stub 目录!! (使用包的其他非开发者客户端)
# 模块中没有 pyi 则创建
def __02():
    for i00, (f_path, f_name, d_rela) in enumerate(__.mods):
        f_name: str = f_name
        f_path: Path = f_path
        i_path = f_path.parent / '{0}{1}'.format(f_name, __.suffix_1)
        s_path = __.stub / d_rela / ('{0}{1}'.format(f_name, __.suffix_1))

        if not i_path.exists():
            __storage(i_path, [])

        __.mods[i00].extend([i_path, s_path])

    # 复制 __type__.py 到 stub
    t_path = __.root / '__type__.py'

    if t_path.exists() and __.stub.exists():
        copy(t_path, __.stub / t_path.name)


# 暂时废弃, 开发时不再复制
# 复制 pyi 文件 (stub 目录, 该目录与 src 目录是兄弟关系)
# i_path 不存在或 空文件不要复制
def __03():
    from os.path import getsize

    for i00, (f_path, f_name, d_rela, i_path, s_path) in enumerate(__.mods):
        if not s_path.parent.exists():
            s_path.parent.mkdir(parents=True, exist_ok=True)

        if i_path.exists() and getsize(i_path):
            copy(i_path, s_path)


# ----------------------------------------------------------------------------------------------------
__exec(getattr(__, ['a_exec', 'b_exec'][int(__name__ == '__main__')]))
