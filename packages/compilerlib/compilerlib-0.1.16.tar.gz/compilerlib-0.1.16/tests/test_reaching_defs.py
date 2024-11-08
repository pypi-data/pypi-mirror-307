import inspect
from compilerlib.types import *
from compilerlib import *
from compilerlib.ast_utils import *

def foo(a: Array(2), b: Array(2), r: Array(2), iters: int):
    i = 0
    while i < iters:
        __v1 = matmul(a, b)
        __v2 = div(1.0, __v1)
        b = matmul(r, __v2)
        i += 1
        if i == 10:
            print(i)
    return b

def gcd(a: int, b: int):
    c = a
    d = b
    if c == 0:
        return d
    while d != 0:
        if c > d:
            c = c - d
        else:
            d = d - c
    return c

tree = func_to_ast(gcd)


tree = apply_transform_on_ast("attach_preds_succs_exit_based", tree)
#tree = apply_transform_on_ast("show_preds_succs", tree)
tree = apply_transform_on_ast("attach_reaching_defs", tree)
tree = apply_transform_on_ast("show_reaching_defs", tree)
print(ast_to_code(tree))