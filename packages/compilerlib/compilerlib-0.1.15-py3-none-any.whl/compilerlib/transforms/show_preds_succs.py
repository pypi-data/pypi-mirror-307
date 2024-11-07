import ast_comments as ast

class ShowPredsSuccs(ast.NodeTransformer):
    def visit(self, node):
        if hasattr(node, 'cfg_id') and not isinstance(node, ast.FunctionDef):
            #print('predecessors:', [n.cfg_id for n in node.predecessors])
            #print('successors:', [n.cfg_id for n in node.successors])
            #node.type_comment = f'id: {node.cfg_id}, preds: {[n.cfg_id for n in node.predecessors]}, succs: {[n.cfg_id for n in node.successors]}'
            #node.type_comment = f'id: {node.cfg_id}, successors: {[n.cfg_id for n in node.successors]}'
            comment = f'# id: {node.cfg_id}, successors: {[n.cfg_id for n in node.successors]}'
            node.comment = ast.Comment(value=comment, inline=False)

        self.generic_visit(node)

        if hasattr(node, 'comment'):
            return [node.comment, node]
        else:
            return node

def transform(node):
    return ShowPredsSuccs().visit(node)