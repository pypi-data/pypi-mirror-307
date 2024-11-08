import ast_comments as ast

class StripCommentNodes(ast.NodeTransformer):
    def visit_Comment(self, node):
        return None

def transform(node):
    return StripCommentNodes().visit(node)