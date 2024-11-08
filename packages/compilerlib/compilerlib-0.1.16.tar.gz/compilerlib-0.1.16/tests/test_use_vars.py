import inspect
from compilerlib.types import *
from compilerlib import *

def foo(a: Array(2), b: Array(2)):
    return a * 0.2 + b * 0.8

tree = func_to_ast(foo)
tree = apply_transform_on_ast("to_single_op_form", tree)
tree = apply_transform_on_ast("attach_preds_succs_exit_based", tree)
tree = apply_transform_on_ast("attach_reaching_defs", tree)
tree = apply_transform_on_ast("show_reaching_defs", tree)
print(ast_to_code(tree))