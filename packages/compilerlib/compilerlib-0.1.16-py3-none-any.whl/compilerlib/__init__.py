import ast_comments as ast
import inspect
import importlib
import compilerlib.ast_utils as ast_utils

def compile(f):
    '''
    Compiles a function with type annotations. `f` will be compiled before it's used.
    '''
    

def jit(f):
    '''
    Compiles a function with type annotations. `f` is compiled upon its first invocation.
    '''

def func_to_ast(f):
    return code_to_ast(inspect.getsource(f))
    # tree = ast.parse(inspect.getsource(f))
    # tree = apply_transform_on_ast("convert_augassign_to_assign", tree)
    # return tree.body[0]

def code_to_ast(src):
    tree = ast.parse(src).body[0]
    tree = apply_transform_on_ast("convert_augassign_to_assign", tree)
    return tree

def ast_to_code(tree):
    return ast.unparse(tree)

def apply_transform_on_ast(m, tree):
    assert inspect.ismodule(m) or isinstance(m, str)
    if isinstance(m, str):
        module_name = f"compilerlib.transforms.{m}"
        m = importlib.import_module(module_name)
    tree = m.transform(tree)
    return tree

def apply_transform_on_src(m, src):
    tree = apply_transform_on_ast(m, ast.parse(src).body[0])
    newsrc = ast.unparse(tree)
    return newsrc

def apply_analysis_on_ast(m, tree):
    pass

def apply_optimization_on_ast(m, tree):
    assert inspect.ismodule(m) or isinstance(m, str)
    if isinstance(m, str):
        module_name = f"compilerlib.optimizations.{m}"
        m = importlib.import_module(module_name)
    tree = m.optimize(tree)
    return tree

def apply_optimization_on_src(m, src):
    tree = apply_optimization_on_ast(m, ast.parse(src).body[0])
    newsrc = ast.unparse(tree)
    return newsrc