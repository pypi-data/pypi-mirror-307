import ast_comments as ast

class RemoveUnusedDefs(ast.NodeTransformer):

    def visit(self, node):
        if hasattr(node, 'cfg_id') and not isinstance(node, ast.FunctionDef):
            if hasattr(node, 'def_vars') and len(node.defuse) == 0:
                return

        self.generic_visit(node)
        return node

def transform(node):
    return RemoveUnusedDefs().visit(node)