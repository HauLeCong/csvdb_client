
class ASTPrinter:
    
    def __init__(self):
        pass
    
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
            case "Select":
                return self.handle_select_node
            case "ColumnList":
                return self.handle_column_list_node
            case "Column":
                return self.handle_column_node
            case "Expr":
                return self.handle_expr_node
            case "ExprAdd":
                return self.handle_expr_add_node
            case "ExprMulti":
                return self.handle_expr_multi_node
            case "ExprValue":
                return self.handle_expr_value_node
            case "Value":
                return self.handle_value_node
            case "Predicate":
                return self.handle_predicate_node
            case "PredicateOr":
                return self.handle_predicate_or_node
            case "PredicateAnd":
                return self.handle_predicate_and_node
            case "PredicateNot":
                return self.handle_predicate_not_node
            case "PredicateCompare":
                return self.handle_predicate_compare_node
            case "PredicateParent":
                return self.handle_predicate_parent_node

     
    def handle_column_list_node(self, column_list_node, spacing: int=0):
        if column_list_node.operator:
            print (f"""{" | "*spacing}{column_list_node.__class__.__name__} opr. {column_list_node.operator.value} """)
        else:
            print (f"""{" | "*spacing}{column_list_node.__class__.__name__}""")
        spacing += 1
        self.visit(column_list_node.left, spacing = spacing)
        if column_list_node.right:
            self.visit(column_list_node.right, spacing = spacing)
            return
        return  
     
    def handle_column_node(self, column_node, spacing: int=0):
        print (f"""{" | "*spacing}{column_node.__class__.__name__}""") 
        spacing += 1
        self.visit(column_node.expr, spacing = spacing)
        return
        
    def handle_expr_node(self, expr_node, spacing: int=0):
        print (f"""{" | "*spacing} {expr_node.__class__.__name__}""")
        spacing += 1
        self.visit(expr_node.expr, spacing = spacing)
        return
    
    def handle_expr_add_node(self, expr_add_node, spacing: int=0):
        if expr_add_node.operator:
            print (f"""{" | "*spacing}{expr_add_node.__class__.__name__} opr. {expr_add_node.operator.value} """)
        else:
            print (f"""{" | "*spacing}{expr_add_node.__class__.__name__}""")
        spacing += 1
        self.visit(expr_add_node.left, spacing = spacing)
        if expr_add_node.right:
            self.visit(expr_add_node.right, spacing = spacing)
            return
        return
    
    def handle_expr_multi_node(self, expr_multi_node, spacing: int=0):
        if expr_multi_node.operator:
            print (f"""{" | "*spacing}{expr_multi_node.__class__.__name__} opr. {expr_multi_node.operator.value} """)
        else:
            print (f"""{" | "*spacing}{expr_multi_node.__class__.__name__}""")
        spacing += 1
        self.visit(expr_multi_node.left, spacing = spacing)
        if expr_multi_node.right:
            self.visit(expr_multi_node.right, spacing = spacing)
            return
        return
    
    def handle_expr_value_node(self, expr_value_node, spacing: int=0):
        if hasattr(expr_value_node.expr, "left"):
            print(f"""{" | "*spacing}{expr_value_node.__class__.__name__}""")
            spacing += 1
            self.visit(expr_value_node.expr, spacing = spacing)
            return
        else:
            print(f"""{" | "*spacing}{expr_value_node.__class__.__name__}: {expr_value_node.expr}""")
            return 
     
    def handle_predicate_node(self, predicate_node, spacing: int = 0):
        print (f"""{" | "*spacing} {predicate_node.__class__.__name__}""")
        spacing += 1
        self.visit(predicate_node.expr, spacing = spacing)
        return  
    
    def handle_predicate_or_node(self, predicate_or_node, spacing:int = 0):
        if predicate_or_node.operator:
            print (f"""{" | "*spacing} {predicate_or_node.__class__.__name__} opr. {predicate_or_node.operator.value} """)
        else:
            print (f"""{" | "*spacing} {predicate_or_node.__class__.__name__}""")
        spacing += 1
        self.visit(predicate_or_node.left, spacing = spacing)
        if predicate_or_node.right:
            self.visit(predicate_or_node.right, spacing = spacing)
            return
        return
    
    def handle_predicate_and_node(self, predicate_and_node, spacing: int = 0):
        if predicate_and_node.operator:
            print (f"""{" | "*spacing} {predicate_and_node.__class__.__name__} opr. {predicate_and_node.operator.value} """)
        else:
            print (f"""{" | "*spacing} {predicate_and_node.__class__.__name__}""")
        spacing += 1
        self.visit(predicate_and_node.left, spacing = spacing)
        if predicate_and_node.right:
            self.visit(predicate_and_node.right, spacing = spacing)
            return
        return
    
    def handle_predicate_not_node(self, predicate_not_node, spacing: int = 0):
        if predicate_not_node.operator:
            print(f"""{" | "*spacing} {predicate_not_node.__class__.__name__} opr. {predicate_not_node.operator.value} """)
        else:
            print (f"""{" | "*spacing} {predicate_not_node.__class__.__name__}""")
        spacing += 1
        self.visit(predicate_not_node.expr, spacing = spacing)
        return
    
    def handle_predicate_compare_node(self, predicate_compare_node, spacing: int = 0):
        if predicate_compare_node.operator:
            print (f"""{" | "*spacing} {predicate_compare_node.__class__.__name__} opr. {predicate_compare_node.operator.value} """)
        else:
            print (f"""{" | "*spacing} {predicate_compare_node.__class__.__name__}""")
        spacing += 1
        self.visit(predicate_compare_node.left, spacing = spacing)
        if predicate_compare_node.right:
            self.visit(predicate_compare_node.right, spacing = spacing)
            return
        return
    
    def handle_predicate_parent_node(self, predicate_parent_node, spacing: int = 0):
       
        print (f"""{" | "*spacing} {predicate_parent_node.__class__.__name__}""")
        spacing += 1
        self.visit(predicate_parent_node.expr, spacing = spacing)
        return 