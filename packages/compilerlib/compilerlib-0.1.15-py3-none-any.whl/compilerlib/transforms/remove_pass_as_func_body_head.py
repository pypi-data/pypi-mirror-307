import ast

class RemovePassAsFuncBodyHead(ast.NodeTransformer):
    def visit_FunctionDef(self, N: ast.FunctionDef):
        if isinstance(N.body[0], ast.Pass):
            N.body.pop(0)
        return N