
from .execution_node import SelectExecNode, ScanExecNode, ProjectExecNode
from functools import partial

class QueryPlanner:
    """
        This class convert a AST to plan of relational algebra

    """
    
    def __init__(self):
        pass
    
    def get_handler(self, node_type):
        
        match node_type:
            case "Arimethic":
                return self.handle_arimethic_node
            case "Factor":
                return self.handle_factor_node
            case "Term":
                return self.handle_term_node
            case "Logical":
                return self.handle_logical_node
            case "Select":
                return self.handle_select_node
            case "From":
                return self.handle_from_node
            case "ColumnWildCard":
                return self.handle_column_wild_card_node
            case "ColumnName":
                return self.handle_column_name_node
            case "ColumnList":
                return self.handle_column_list_node
            case "Column":
                return self.handle_column_node 
            case "Expr":
                return self.handle_expr_node                   
    
    def visit(self, node):
        handler = self.get_handler(node.type)
        return handler(node)
        
    def handle_logical_node(self, logical_node):
        #left, right, operator
        left_value = self.visit(logical_node.left)
        right_value = self.visit(logical_node.right)
        if logical_node.operator == "AND":
            return left_value and right_value
        
    def handle_arimethic_node(self, arimethic_node):
        print(arimethic_node)
        left_value = self.visit(arimethic_node.left)
        if arimethic_node.right:
            right_value = self.visit(arimethic_node.right)
            if arimethic_node.operator.value == '+':
                return left_value + right_value 
            elif arimethic_node.operator.value == "-":
                return left_value - right_value
        return left_value
        
    def handle_term_node(self, term_node):
        left_value = self.visit(term_node.left)
        if term_node.right:
            right_value = self.visit(term_node.right)
            if term_node.operator.value == "*":
                return left_value * right_value
            elif term_node.operator.value == "/":
                return left_value / right_value
        return left_value
    
    def handle_factor_node(self, factor_node):
        if not hasattr(factor_node.expr, "left"):
            return factor_node.expr
        return self.visit(factor_node.expr)
    
    def handle_ast_node(self, ast_node):
        return self.visit(ast_node.expr)
    
    def handle_column_name_node(self, column_name_node):
        return column_name_node.expr
    
    def handle_column_wild_card_node(self, wild_card_node):
        return wild_card_node.expr
    
    def handle_column_list_node(self, column_list_node):
        result = []
        left_value = self.visit(column_list_node.left)
        result.append(left_value)
        if column_list_node.right:
            right_value = self.visit(column_list_node.right)
            result.append(right_value)
            return result
        
        return result
    
    def handle_column_node(self, column_node):
        return self.visit(column_node.expr)
        
    def handle_expr_node(self, expr_node):
        return self.visit(expr_node.expr)
    
    def handle_select_node(self, select_node) -> ProjectExecNode:
        project_list =  self.visit(select_node.column_list)   
        from_clause = self.visit(select_node.from_clause)
        return ProjectExecNode(
            child = from_clause,
            projects = project_list
        )
            
    def handle_where_node(self, where_node) -> SelectExecNode:
        pass
    
    def handle_from_node(self, from_node) -> ScanExecNode:
        table = from_node.expr
        return ScanExecNode(table=table)
    
    def build(self, ast):
        self.visit(ast)
    