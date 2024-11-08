import ast
from copy import deepcopy

class RewriteAugAssign(ast.NodeTransformer):
    def visit_AugAssign(self, node):
        left = node.target
        right = node.value        
        leftcopy = deepcopy(left)
        leftcopy.ctx = ast.Load()
        newnode = ast.Assign(targets=[left], 
                    value=ast.BinOp(left=leftcopy, op=node.op, right=node.value), 
                    lineno=node.lineno)
        return newnode

def transform(node):
    return RewriteAugAssign().visit(node)