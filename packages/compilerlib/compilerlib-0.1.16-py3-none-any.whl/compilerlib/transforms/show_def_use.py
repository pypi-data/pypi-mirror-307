import ast_comments as ast

class ShowDefUse(ast.NodeTransformer):

    def visit(self, node):
        if hasattr(node, 'cfg_id') and not isinstance(node, ast.FunctionDef):
            if len(node.defuse) > 0:
                comment = f'# node {node.cfg_id}, used in: {[x.cfg_id for x in node.defuse]}'
            elif hasattr(node, 'def_vars'):
                comment = f'# node {node.cfg_id}, def unused'
            else:
                comment = f'# node {node.cfg_id}'
            node.comment = ast.Comment(value=comment, inline=False)

        self.generic_visit(node)

        if hasattr(node, 'comment'):
            return [node.comment, node]
        else:
            return node

def transform(node):
    return ShowDefUse().visit(node)