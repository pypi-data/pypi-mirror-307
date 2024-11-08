import ast

class InsertPassAsFuncBodyHead(ast.NodeTransformer):
    '''
    This pass simplifies control flow analysis on the function body.
    '''
    def visit_FunctionDef(self, N: ast.FunctionDef):
        if not isinstance(N.body[0], ast.Pass):
            N.body.insert(0, ast.Pass())
        return N

def transform(tree):
    return InsertPassAsFuncBodyHead().visit(tree)