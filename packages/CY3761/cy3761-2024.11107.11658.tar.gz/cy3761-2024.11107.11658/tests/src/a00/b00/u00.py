from src import *

def fn_03(x, y):
    """
    这里能设置函数说明, 在 py 文件, 函数声明部分, 非函数类型部分
    """
    if isinstance(x, int) and isinstance(y, int):
        return x + y

    if isinstance(x, str) and isinstance(y, str):
        return x + y

    raise TypeError('Unsupported operand types')


# print(fn_00(1, 2))

# 默认
# 模块名 (目录与文件名), 首字符不能是数字, 具有 pyi 需要 同目录和同文件名
# load_stubs (stubs: 存根) 做一个自动化工具,
# 用于将 stubs 目录下的 *.pyi 复制到 当前文件夹下, 使其达到 py 与 pyi 同目录和同文件名
# pyi 开发和调用时 代码提示使用, 发布到线上还未知处理情况 setup 方式
# 获取当前文件路径, 目录路径, 文件名, 存储 *.pyi 文件位置
# 判断 存储 *.pyi 文件位置, 是否有对应的文件, 没有就创建, 并且设置好修改的行号 (在py注入stubs文件名)
# pyi 只在 stubs 目录下, 文件名需要处理
# 每次使用执行会处理 __init__ 通过这个进行处理 存入和更新 pyi
# 没有执行 I:\33008\项目\CY3761\tests\src\__init__.py

# 可以无极目录架构, 但目录首字符不能是数字, 且 py 与 pyi 需同目录和同文件名

# 在调用时, 虽然支持, 没有出现提示错误, 但类型 str 还是没有显示
# 通过变量赋值方式, 变量能够识别其变量, 但函数体部分不能识别
# 暂时成功是 py 与 pyi 同目录同名, 其余不成功

# __init__.py 没有执行, 本模块直接运行无效, 导入本模块再运行才有效

v01 = fn_03('a', 'b')
# print(v01)

if __name__ == '__main__':
    print('u00.py', fn_00)
    print('u00.py', fn_01)
    print('u00.py', fn_02)
    print('u00.py', fn_03)
