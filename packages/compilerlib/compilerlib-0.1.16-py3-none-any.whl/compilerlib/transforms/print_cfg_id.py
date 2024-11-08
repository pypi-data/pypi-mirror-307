import ast

class PrintCFGId(ast.NodeVisitor):
    def visit(self, node):
        if hasattr(node, 'cfg_id'):
            print(f"node {node.cfg_id}: {ast.unparse(node).split('\n')[0]}")
        return self.generic_visit(node)

def transform(node):
    visitor = PrintCFGId()
    visitor.visit(node)
    return node