import ast

class RemoveUnreachableCode(ast.NodeTransformer):
    def visit(self, node):
        if hasattr(node, 'cfg_id') and not isinstance(node, ast.FunctionDef) and len(node.predecessors) == 0:
            return
        else:
            self.generic_visit(node)
            return node

def transform(tree):
    return RemoveUnreachableCode().visit(tree)