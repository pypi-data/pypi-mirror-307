# https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
# 类型提示速查表

# Variables | 变量
# 以下所示的大多数类型注解在技术上都是多余的,
# 因为 mypy 通常可以从变量的值中推断出其类型.
# 有关类型推断和类型注解的更多详细信息, 请参阅相关内容.
# 相关内容
# https://mypy.readthedocs.io/en/stable/type_inference_and_annotations.html#type-inference-and-annotations

# 这是声明变量类型的方式
v00: int = 1

# 您无需初始化变量即可对其进行注释
# Ok (在分配之前在运行时没有值)
v01: int

# 这样做在条件分支中可能很有用
v02: bool = True if v00 < 18 else False
v03 = True if v00 < 18 else False

# Useful built-in types | 内置类型使用指南

# 对于大多数类型, 只需在 annotation 中使用类型的名称
# 请注意, mypy 通常可以从变量的值中推断出变量的类型,
# 所以从技术上讲, 这些注解是多余的
# 这些都是 变量 = 字面量 (没有变量名或表达式, 如函数)

v04: int = 1
v05: float = 1.0
v06: bool = True
v07: str = 'test'
v08: bytes = b'test'

# 对于 Python 3.9+ 上的集合, 集合项的类型位于括号中
v09: list[int] = [1]
v10 = [1]  # v10: list[int] = [1]
v11: set[int] = {1, 2}
v12 = {1, 2}  # v12: set[int] = {1, 2}

# 对于 Map (映射), 我们需要 key 和 values 的类型
# 使用花括号包裹整个映射, 键使用引号包裹为真实键, 不使用则可能是动态键, 键是一个变量
v13: dict[str, float] = {'field': 2.0}  # Python 3.9+
v14 = {'field': 2.0}  # v14: dict[str, float] = {'field': 2.0}

# 对于固定大小的元组, 我们指定所有元素的类型
v15: tuple[int, str, float] = (3, 'yes', 7.5)  # Python 3.9+
v16 = (3, 'yes', 7.5)  # v16: tuple[int, str, float] = (3, 'yes', 7.5)

# 对于可变大小的元组, 我们使用一种类型和省略号
v17: tuple[int, ...] = (1, 2, 3)  # Python 3.9+
v18 = (1, 2, 3)  # v18: tuple[int, int, int] = (1, 2, 3) # 可变的类型注解不同了

# 在 Python 3.8 及更早版本中, 集合类型的名称为
# 首字母大写, 并且类型是从 'typing' 模块导入的
from typing import List, Set, Dict, Tuple

v19: List[int] = [1]
v20: Set[int] = {6, 7}
v21: Dict[str, float] = {'field': 2.0}
v22: Tuple[int, str, float] = (3, 'yes', 7.5)
v23: Tuple[int, ...] = (1, 2, 3)

from typing import Union, Optional

# 在 Python 3.10+ 上, 使用 | 运算符 (如果某些内容可能是几种类型之一)
v24: list[int | str] = [3, 5, 'test', 'fun']  # Python 3.10+
v25 = [3, 5, 'test', 'fun']  # v25: list[int | str] = [3, 5, 'test', 'fun']
# 在早期版本中, 使用 Union
v26: list[Union[int, str]] = [3, 5, "test", "fun"]

# 使用 X | None 表示在 Python 3.10+ 上可以是 None 的值
# 在 3.9 及更早版本中使用 Optional[X]; Optional[X] 就像 'X | None'
from random import randint

v27: str | None = 'something' if randint(1, 2) % 2 == 0 else None
# v28: str | None = 'something' if randint(1, 2) % 2 == 0 else Non
v28 = 'something' if randint(1, 2) % 2 == 0 else None

if v28 is not None:
    # Mypy 明白 x 在这里不会是 None, 因为 if 语句
    print(v28.upper())
# 如果你知道一个值永远不能是 None, 因为某些逻辑是 mypy 没有的
# 理解, 使用 assert

assert v28 is not None
print(v28.upper())  # 提示始终 v28: str | None, 而不是 v28:str

# Functions 功能区
# https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html

# from collections.abc import Sequence | Sequence: 序列类型, 字符串, 元组, 列表, 字典
# 类型别名可以用 TypeAlias 来标记，以显式指明该语句是类型别名声明，而不是普通的变量赋值
