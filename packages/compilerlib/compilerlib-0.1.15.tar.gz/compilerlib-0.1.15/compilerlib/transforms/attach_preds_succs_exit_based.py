import ast
from .attach_cfg_id import AttachCFGId
from .strip_comment_nodes import StripCommentNodes

class InitializePredsSuccsProperty(ast.NodeTransformer):
    def visit(self, N):
        N.predecessors = []
        N.successors = []
        self.generic_visit(N)
        return N

class AttachPredsSuccsProperty(ast.NodeTransformer):
    def __init__(self):
        self.context = {
            'function': [],
            'loop': []
        }

    def push_func_context(self, N):
        self.context['function'].append(N)

    def pop_func_context(self):
        self.context['function'].pop(-1)

    def push_loop_context(self, N):
        self.context['loop'].append(N)

    def pop_loop_context(self):
        self.context['loop'].pop(-1)

    def context_get_top_func(self):
        return self.context['function'][-1]

    def context_get_top_loop(self):
        return self.context['loop'][-1]

    def visit_FunctionDef(self, N: ast.FunctionDef):
        self.push_func_context(N)
        N.exits = []
        self.try_add_edge(N, N.body[0])
        self.visit_seq_body(N.body, N)
        self.pop_func_context()
        return N

    def visit_seq_body(self, body, context):
        '''
        Sequentially add an edge between a node and its previous nodes.
        This function returns a list of nodes that should be the predecessors of 
        the node that follows in the upper-level body. 
        '''
        cur_exits = []
        for i in range(len(body)):
            child = body[i]
            cur_exits = [child]
            # No need to try to link `child` with the next node if `child` is a return, break or continue
            if isinstance(child, ast.Return):
                self.context_get_top_func().exits.append(child)
                cur_exits = []
                break
            elif isinstance(child, ast.Break):
                self.context_get_top_loop().breaks.append(child)
                cur_exits = []
                break
            elif isinstance(child, ast.Continue):
                # Add back edge
                self.try_add_edge(child, self.context_get_top_loop())
                cur_exits = []
                break

            if isinstance(child, ast.While):
                cur_exits = self.visit_While(child)

            if isinstance(child, ast.If):
                cur_exits = self.visit_If(child)
            
            if i + 1 < len(body):
                for t in cur_exits:
                    self.try_add_edge(t, body[i+1])
        return cur_exits

    def visit_While(self, N):
        self.push_loop_context(N)
        N.breaks = []
        self.try_add_edge(N, N.body[0])
        body_exits = self.visit_seq_body(N.body, N)
        # Add back edges for while loop
        for t in body_exits:
            self.try_add_edge(t, N)
        self.pop_loop_context()
        return [N] + N.breaks

    def visit_If(self, N):
        self.try_add_edge(N, N.body[0])
        if len(N.orelse) > 0:
            self.try_add_edge(N, N.orelse[0])

        body_exits = []
        body_exits += self.visit_seq_body(N.body, N)
        if len(N.orelse) > 0:
            body_exits += self.visit_seq_body(N.orelse, N)
        else:
            body_exits += [N]
        return body_exits        
        
    def get_exits_to_next(self, N):
        if isinstance(N, ast.While):
            return [N] + N.breaks
        elif isinstance(N, ast.If):
            exits_to_next = self.get_exits_to_next(N.body[-1])
            if len(N.orelse) > 0:
                exits_to_next += self.get_exits_to_next(N.orelse[-1])
            else:
                # directly exit from the condition node
                exits_to_next += [N]
            return exits_to_next
        else:
            return [N]

    def try_add_edge(self, this, that):
        if isinstance(this, ast.Return):
            return
            
        this.successors.append(that)
        that.predecessors.append(this)


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
    tree = StripCommentNodes().visit(tree)
    tree = AttachCFGId().visit(tree)
    tree = InitializePredsSuccsProperty().visit(tree)
    tree = AttachPredsSuccsProperty().visit(tree)
    #tree = DumpPredsSuccsProperty().visit(tree)
    return tree