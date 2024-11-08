import ast_comments as ast
import json

class ShowReachingDefs(ast.NodeTransformer):
    def reaching_defs_to_string(self, defs):
        items = []
        for k in defs:
            items.append(f'{k}=>{[x.cfg_id for x in defs[k]]}')
        return ', '.join(items)

    def visit(self, node):
        if hasattr(node, 'cfg_id'):
            if isinstance(node, ast.FunctionDef):
                comment = f'# node {node.cfg_id} is the function declaration, which defines the arguments'
            else:
                inset = node.usedef['in']
                comment = f'# node {node.cfg_id}, use_defs: {self.reaching_defs_to_string(inset)}'
            node.comment = ast.Comment(value=comment, inline=False)

        self.generic_visit(node)

        if hasattr(node, 'comment'):
            return [node.comment, node]
        else:
            return node

def transform(node):
    return ShowReachingDefs().visit(node)