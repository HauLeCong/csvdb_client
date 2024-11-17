
class ASTPrinter:
    
    def __init__(self):
        self.tree_level = 1
        self.node_prefix = "+-"
    
    def visit(self, node, *args, **kwargs):
        handler = self.get_node_handler(node.type)
        return handler(node, *args, **kwargs)
    
    def get_node_handler(self, node_type):
        match node_type:
            case "Arimethic":
                return self.handle_arimethic_node
            case "Term":
                return self.handle_term_node
            case "Factor":
                return self.handle_factor_node
            
    def handle_arimethic_node(self, arimethic_node ,level_print: str, spacing: int):
        sub_node_level = 1
        if arimethic_node.operator:
            print (f"""{" | "*spacing}{level_print} {arimethic_node.__class__.__name__}opr. {arimethic_node.operator.value} """)
        else:
            print (f"""{" | "*spacing}{level_print} {arimethic_node.__class__.__name__}""")
        spacing += 1
        self.visit(arimethic_node.left, level_print = f"{level_print}.{sub_node_level}", spacing = spacing)
        if arimethic_node.right:
            self.visit(arimethic_node.right, level_print = f"{level_print}.{sub_node_level + 1}", spacing = spacing)
            return
        return
    
    def handle_term_node(self, term_node, level_print: str, spacing: int):
        sub_node_level = 1
        if term_node.operator:
            print (f"""{" | "*spacing}{level_print} {term_node.__class__.__name__}opr. {term_node.operator.value} """)
        else:
            print (f"""{" | "*spacing}{level_print} {term_node.__class__.__name__}""")
        spacing += 1
        self.visit(term_node.left, level_print = f"{level_print}.{sub_node_level}", spacing = spacing)
        if term_node.right:
            self.visit(term_node.right, level_print = f"{level_print}.{sub_node_level + 1}", spacing = spacing)
            return
        return
    
    def handle_factor_node(self, factor_node, level_print: str, spacing: int):
        sub_node_level = 1
        if hasattr(factor_node.expr, "left"):
            print(f"""{" | "*spacing}{level_print} {factor_node.__class__.__name__}""")
            spacing += 1
            self.visit(factor_node.expr, level_print = f"{level_print}.{sub_node_level + 1}", spacing = spacing)
            return
        else:
            print(f"""{" | "*spacing}{level_print} {factor_node.__class__.__name__}: {factor_node.expr}""")
            return 