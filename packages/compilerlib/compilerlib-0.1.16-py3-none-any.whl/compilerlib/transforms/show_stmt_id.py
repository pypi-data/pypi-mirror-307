import ast
from compilerlib.ast_utils import *

class ShowStmtID(ast.NodeTransformer):
    '''
    Note that return statement will have a stmt_id but it won't show up after unparse()
    '''
    def visit(self, node):
        if hasattr(node, 'stmt_id'):
            node.type_comment = f'stmt_id: {node.stmt_id}'
        self.generic_visit(node)
        return node

def transform(tree):
    return ShowStmtID().visit(tree)