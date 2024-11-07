from compilerlib import apply_transform_on_ast

def transform(tree):
    tree = apply_transform_on_ast("convert_augassign_to_assign", tree)
    return tree