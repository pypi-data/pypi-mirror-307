
from compilerlib.types import *
from compilerlib import *
from compilerlib.ast_utils import *

def foo(a: Array(2), b: Array(2), r: Array(2), iters: int):
    i = 0
    while i < iters:
        __v1 = matmul(a, b)
        __v2 = div(1.0, __v1)
        b = matmul(r, __v2)
        if i == 10:
            b = matmul(r, __v2) + i
        else:
            b = matmul(r, __v2)
        i = i + 1
    return b
    b = b + 1
    return b

tree = func_to_ast(foo)
tree = apply_transform_on_ast("attach_preds_succs_exit_based", tree)
tree = apply_transform_on_ast("attach_reaching_defs", tree)
tree = apply_transform_on_ast("remove_unreachable_code", tree)
tree = apply_transform_on_ast("remove_unused_defs", tree)
tree = apply_transform_on_ast("show_cfg_successors", tree)

print(ast_to_code(tree))