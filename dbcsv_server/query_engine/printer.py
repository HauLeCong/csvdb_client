
class ASTPrinter:
    
    def __init__(self):
        pass
    
    def print_node(self, node, *args, **kwargs):
        handler = self.get_node_handler(node.type)
        return handler(node, *args, **kwargs)
    
    def get_node_handler(self, node_type):
        match node_type:
            case "AST":
                return self.handle_ast_node
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
            case "Select":
                return self.handle_select_node
            case "Where":
                return self.handle_where_node
            case "From":
                return self.handle_from_node
            case "ColumnWildCard":
                return self.handle_column_wildcard

    def handle_ast_node(self, ast_node, spacing: int=0):
        print (f"""{" | "*spacing}{ast_node.__class__.__name__}""")
        init_spacing = spacing
        spacing = init_spacing + 1
        self.print_node(ast_node.nodes, spacing)
    
    def handle_select_node(self, select_node, spacing: int=0):
        inital_spacing = spacing    
        print (f"""{" | "*spacing}{select_node.__class__.__name__}""")
        spacing = inital_spacing + 1
        self.print_node(select_node.column_list, spacing)
        if select_node.from_clause:
            spacing = inital_spacing + 1
            self.print_node(select_node.from_clause, spacing)
            if select_node.where_clause:
                spacing = inital_spacing + 1
                self.print_node(select_node.where_clause, spacing)
     
    def handle_column_list_node(self, column_list_node, spacing: int=0):
        if column_list_node.operator:
            print (f"""{" | "*spacing}{column_list_node.__class__.__name__} opr. {column_list_node.operator.value} """)
        else:
            print (f"""{" | "*spacing}{column_list_node.__class__.__name__}""")
        spacing += 1
        self.print_node(column_list_node.left, spacing = spacing)
        if column_list_node.right:
            self.print_node(column_list_node.right, spacing = spacing)
            return
        return 

    def handle_where_node(self, where_node, spacing: int=0):
        print (f"""{" | "*spacing}{where_node.__class__.__name__}""")
        spacing += 1
        self.print_node(where_node.expr, spacing)
        return
    
    def handle_from_node(self, from_node, spacing: int=0):
        initial_spacing = spacing
        print (f"""{" | "*spacing}{from_node.__class__.__name__} """)
        spacing = initial_spacing + 1
        print (f"""{" | "*spacing}{from_node.database.__class__.__name__}: {from_node.database.expr[1]}""")
        spacing = initial_spacing + 1
        print (f"""{" | "*spacing}{from_node.table_name.__class__.__name__}: {from_node.table_name.expr[1]}""")
        return
     
    def handle_column_node(self, column_node, spacing: int=0):
        print (f"""{" | "*spacing}{column_node.__class__.__name__}""") 
        spacing += 1
        self.print_node(column_node.expr, spacing = spacing)
        return
    
    def handle_column_wildcard(self, column_wildcard_node, spacing: int=0):
        print (f"""{" | "*spacing}{column_wildcard_node.__class__.__name__}""") 
        return
        
    def handle_expr_node(self, expr_node, spacing: int=0):
        print (f"""{" | "*spacing} {expr_node.__class__.__name__}""")
        spacing += 1
        self.print_node(expr_node.expr, spacing = spacing)
        return
    
    def handle_expr_add_node(self, expr_add_node, spacing: int=0):
        if expr_add_node.operator:
            print (f"""{" | "*spacing}{expr_add_node.__class__.__name__} opr. {expr_add_node.operator.value} """)
        else:
            print (f"""{" | "*spacing}{expr_add_node.__class__.__name__}""")
        spacing += 1
        self.print_node(expr_add_node.left, spacing = spacing)
        if expr_add_node.right:
            self.print_node(expr_add_node.right, spacing = spacing)
            return
        return
    
    def handle_expr_multi_node(self, expr_multi_node, spacing: int=0):
        if expr_multi_node.operator:
            print (f"""{" | "*spacing}{expr_multi_node.__class__.__name__} opr. {expr_multi_node.operator.value} """)
        else:
            print (f"""{" | "*spacing}{expr_multi_node.__class__.__name__}""")
        spacing += 1
        self.print_node(expr_multi_node.left, spacing = spacing)
        if expr_multi_node.right:
            self.print_node(expr_multi_node.right, spacing = spacing)
            return
        return
    
    def handle_expr_value_node(self, expr_value_node, spacing: int=0):
        if hasattr(expr_value_node.expr, "left"):
            print(f"""{" | "*spacing}{expr_value_node.__class__.__name__}""")
            spacing += 1
            self.print_node(expr_value_node.expr, spacing = spacing)
            return
        else:
            print(f"""{" | "*spacing}{expr_value_node.__class__.__name__}: {expr_value_node.expr}""")
            return 
     
    def handle_predicate_node(self, predicate_node, spacing: int = 0):
        print (f"""{" | "*spacing} {predicate_node.__class__.__name__}""")
        spacing += 1
        self.print_node(predicate_node.expr, spacing = spacing)
        return  
    
    def handle_predicate_or_node(self, predicate_or_node, spacing:int = 0):
        if predicate_or_node.operator:
            print (f"""{" | "*spacing} {predicate_or_node.__class__.__name__} opr. {predicate_or_node.operator.value} """)
        else:
            print (f"""{" | "*spacing} {predicate_or_node.__class__.__name__}""")
        spacing += 1
        self.print_node(predicate_or_node.left, spacing = spacing)
        if predicate_or_node.right:
            self.print_node(predicate_or_node.right, spacing = spacing)
            return
        return
    
    def handle_predicate_and_node(self, predicate_and_node, spacing: int = 0):
        if predicate_and_node.operator:
            print (f"""{" | "*spacing} {predicate_and_node.__class__.__name__} opr. {predicate_and_node.operator.value} """)
        else:
            print (f"""{" | "*spacing} {predicate_and_node.__class__.__name__}""")
        spacing += 1
        self.print_node(predicate_and_node.left, spacing = spacing)
        if predicate_and_node.right:
            self.print_node(predicate_and_node.right, spacing = spacing)
            return
        return
    
    def handle_predicate_not_node(self, predicate_not_node, spacing: int = 0):
        if predicate_not_node.operator:
            print(f"""{" | "*spacing} {predicate_not_node.__class__.__name__} opr. {predicate_not_node.operator.value} """)
        else:
            print (f"""{" | "*spacing} {predicate_not_node.__class__.__name__}""")
        spacing += 1
        self.print_node(predicate_not_node.expr, spacing = spacing)
        return
    
    def handle_predicate_compare_node(self, predicate_compare_node, spacing: int = 0):
        if predicate_compare_node.operator:
            print (f"""{" | "*spacing} {predicate_compare_node.__class__.__name__} opr. {predicate_compare_node.operator.value} """)
        else:
            print (f"""{" | "*spacing} {predicate_compare_node.__class__.__name__}""")
        spacing += 1
        self.print_node(predicate_compare_node.left, spacing = spacing)
        if predicate_compare_node.right:
            self.print_node(predicate_compare_node.right, spacing = spacing)
            return
        return
    
    def handle_predicate_parent_node(self, predicate_parent_node, spacing: int = 0):
       
        print (f"""{" | "*spacing} {predicate_parent_node.__class__.__name__}""")
        spacing += 1
        self.print_node(predicate_parent_node.expr, spacing = spacing)
        return 