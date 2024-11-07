import ast
from compilerlib.ast_utils import *
from .attach_def_use_vars import AttachDefUseVars

class InitializeInsAndOuts(ast.NodeTransformer):
    def visit(self, N):
        N.usedef = {'in': {}, 'out': {}}        
        self.generic_visit(N)
        return N

class ReachingDefs(ast.NodeVisitor):
    def add_to_out(self, node, var, defining_node):
        node.usedef['out'].setdefault(var, set()).add(defining_node)

    def remove_all_defs_of_var_from_out(self, node, var):
        if var in node.usedef['out']:
            node.usedef['out'].pop(var)
 
    def add_to_in(self, node, var, defining_node):
        node.usedef['in'].setdefault(var, set()).add(defining_node)

    def get_out(self, node):
        return node.usedef['out']

    def get_in(self, node):
        return node.usedef['in']

    def set_out(self, node, out_dict):
        node.usedef['out'] = out_dict

    def set_in(self, node, in_dict):
        node.usedef['in'] = in_dict

    def visit_FunctionDef(self, N):
        for arg in N.args.args:            
            self.add_to_out(N, arg.arg, N)
        
        queue = [] + N.successors
        while len(queue) > 0:
            node = queue.pop(0)
            self.set_in(node, self.merge_defs([self.get_out(x) for x in node.predecessors]))
            old_out = self.get_out(node).copy()
            # This will modify the in and out set in-place
            self.transfer(node) 
            # Add node.successors if its outs set has changed
            if self.get_out(node) != old_out: 
                queue += node.successors
        return N

    def merge_defs(self, defs):
        '''
        Each dict in `defs` maps a variable name to a set of nodes
        '''
        merged_dict = {}
        for d in defs:
            for key, value in d.items():
                merged_dict.setdefault(key, set()).update(value)
        
        return merged_dict

    def transfer(self, node):
        self.set_out(node, self.get_in(node).copy())
        if isinstance(node, ast.Assign):
            var = node.targets[0].id
            # Kill all existing defs of `var`
            self.remove_all_defs_of_var_from_out(node, var)

            # Add new defs
            self.add_to_out(node, var, node)

    def are_dicts_equivalent(self, dict1, dict2):
        # Check if both dictionaries have the same keys
        if dict1.keys() != dict2.keys():
            return False

        # Check if each list for a given key has the same elements (ignoring order)
        for key in dict1:
            if dict1[key] != dict2[key]:
                return False
        
        return True


class PruneReachingDefs(ast.NodeVisitor):
    '''
    This transformer will prune the def sets such that only the definitions of the 
    variables that are used in the node are kept.
    '''
    def visit(self, N):        
        if hasattr(N, 'use_vars'):
            N.usedef['in'] = {k:v for k,v in N.usedef['in'].items() if k in N.use_vars}

        self.generic_visit(N)
        return N


class PrintReachingDefs(ast.NodeTransformer):
    def print_set(self, set, prefix):
        print(f'{prefix}: ', end='')
        for k in set:
            print(f'{k}=>{[x.cfg_id for x in set[k]]}', end=', ')
        print()
        

    def visit(self, N):
        if hasattr(N, 'cfg_id'):
            head = ast.unparse(N).split('\n')[0]
            print(f"node {N.cfg_id}: {head}")
            self.print_set(N.usedef['in'], "in set")
            #self.print_set(N.outs, "outs")
            print()

        self.generic_visit(N)
        return N

        

def transform(node, relevant_only=True):
    node = InitializeInsAndOuts().visit(node)
    node = ReachingDefs().visit(node)
    if relevant_only:
        node = AttachDefUseVars().visit(node)
        node = PruneReachingDefs().visit(node)
    #node = PrintReachingDefs().visit(node)
    return node