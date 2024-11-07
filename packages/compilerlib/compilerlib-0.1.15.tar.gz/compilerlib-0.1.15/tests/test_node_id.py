import inspect
from compilerlib.types import *
from compilerlib import *

def foo(a: Array(2), b: Array(2), r: Array(2), iters: int):
    i = 0
    while i < iters:
        __v1 = matmul(a, b)
        __v2 = div(1.0, __v1)
        b = matmul(r, __v2)
        i = i + 1
    return b

tree = func_to_ast(foo)

tree = apply_transform_on_ast("attach_cfg_id", tree)
tree = apply_transform_on_ast("print_cfg_id", tree)
