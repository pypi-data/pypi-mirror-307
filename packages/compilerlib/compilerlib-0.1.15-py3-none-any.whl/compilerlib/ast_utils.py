import ast_comments as ast

class UnparserWithMoreComments(ast._Unparser):
    def visit_Return(self, node):
        self.fill("return")
        if node.value:
            self.write(" ")
            self.traverse(node.value)
        if type_comment := self.get_type_comment(node):
            self.write(type_comment)

    def visit_While(self, node):
        self.fill("while ")
        self.traverse(node.test)
        with self.block(extra=self.get_type_comment(node)):
            self.traverse(node.body)
        if node.orelse:
            self.fill("else")
            with self.block():
                self.traverse(node.orelse)

    def visit_If(self, node):
        self.fill("if ")
        self.traverse(node.test)
        with self.block(extra=self.get_type_comment(node)):
            self.traverse(node.body)
        # collapse nested ifs into equivalent elifs.
        while node.orelse and len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
            node = node.orelse[0]
            self.fill("elif ")
            self.traverse(node.test)
            with self.block():
                self.traverse(node.body)
        # final else
        if node.orelse:
            self.fill("else")
            with self.block():
                self.traverse(node.orelse)


def unparse(ast_obj):
    # unparser = UnparserWithMoreComments()
    # code = unparser.visit(ast_obj)
    code = ast.unparse(ast_obj)
    newcode = ''
    for line in code.split('\n'):
        newcode += line.replace('# type:', '#', 1) + '\n'
    return newcode

def dump(node):
    print(ast.dump(node))

def new_call(func: str, args: list):
    ret = ast.Call(func = ast.Name(func, ast.Load()), args = args, keywords = [])
    return ret