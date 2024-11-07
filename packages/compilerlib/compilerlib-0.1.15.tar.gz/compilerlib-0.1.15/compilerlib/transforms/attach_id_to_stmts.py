import ast
from compilerlib.ast_utils import *


class AttachIDToStmts(ast.NodeTransformer):
    def __init__(self):
        self.count = 0

    def visit_FunctionDef(self, node):
        node.stmt_id = self.count
        self.count += 1
        
        for child in node.body:
            child.stmt_id = self.count
            self.count += 1

            if isinstance(child, (ast.For, ast.While, ast.If)):
                self.visit(child)

        return node

    def visit_For(self, node):        
        for child in node.body:
            child.stmt_id = self.count
            self.count += 1

            if isinstance(child, (ast.For, ast.While, ast.If)):
                self.visit(child)

        return node

    def visit_If(self, node):
        for child in node.body:
            child.stmt_id = self.count
            self.count += 1

            if isinstance(child, (ast.For, ast.While, ast.If)):
                self.visit(child)

        return node

    def visit_While(self, node):
        for child in node.body:
            child.stmt_id = self.count
            self.count += 1

            if isinstance(child, (ast.For, ast.While, ast.If)):
                self.visit(child)

        return node


def transform(tree):
    return AttachIDToStmts().visit(tree)