import ast
from .attach_cfg_id import AttachCFGId

class InitializePredsSuccsProperty(ast.NodeTransformer):
    def visit(self, N):
        N.predecessors = []
        N.successors = []
        self.generic_visit(N)
        return N

class AttachPredsSuccsProperty(ast.NodeTransformer):
    def visit_FunctionDef(self, N: ast.FunctionDef):
        prevs = [N]
        for i in range(len(N.body)):
            child = N.body[i]
            for prev in prevs:
                prev.successors.append(child)
                child.predecessors.append(prev)
            prevs = [child]

            if isinstance(child, ast.While):
                self.visit_While(child)
                # The last node of a while loop is also a predecessor
                prevs.append(child.body[-1])
        return N

    def visit_While(self, N: ast.While, next_node=None):
        prevs = [N]
        for i in range(len(N.body)):
            child = N.body[i]
            for prev in prevs:
                prev.successors.append(child)
                child.predecessors.append(prev)
            prevs = [child]
        
        # Add back edge
        for prev in prevs:
            prev.successors.append(N)
            N.predecessors.append(prev)        
        return N


def dump_node_preds_succs(N):
    print("node:", ast.unparse(N).split('\n')[0])
    print("predecessors:", [ast.unparse(n).split('\n')[0] for n in N.predecessors])
    print("successors:", [ast.unparse(n).split('\n')[0] for n in N.successors])
    print()

def dump_node_pred_succ_ids(N):
    print("node:", ast.unparse(N).split('\n')[0], N.cfg_id)
    print("predecessors:", [ast.unparse(n).split('\n')[0] for n in N.predecessors], [n.cfg_id for n in N.predecessors])
    print("successors:", [ast.unparse(n).split('\n')[0] for n in N.successors], [n.cfg_id for n in N.successors])
    print()



class DumpPredsSuccsProperty(ast.NodeVisitor):
    def visit(self, N):
        if isinstance(N, (ast.While, ast.Assign)):            
            dump_node_pred_succ_ids(N)
        self.generic_visit(N)
        return N


def transform(tree):
    tree = AttachCFGId().visit(tree)
    tree = InitializePredsSuccsProperty().visit(tree)
    tree = AttachPredsSuccsProperty().visit(tree)
    #tree = DumpPredsSuccsProperty().visit(tree)
    return tree