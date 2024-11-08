from compilerlib.types import *
from compilerlib import *

def foo():
    a = 1
    a = 2
    b = a + 1
    return b

tree = func_to_ast(foo)
tree = apply_transform_on_ast("to_single_op_form", tree)
tree = apply_transform_on_ast("attach_preds_succs", tree)
tree = apply_transform_on_ast("attach_reaching_defs", tree)
tree = apply_transform_on_ast("show_def_use", tree)
print(ast_to_code(tree))