
class ASTHandler:
    
    def get_handler(self, node_type):
        if node_type == "Arimethic":
            return self.handle_arimethic_node
        elif node_type == "Factor":
            return self.handle_factor_node
        elif node_type == "Term":
            return self.handle_term_node
        elif node_type == "Logical":
            return self.handle_logical_node
    
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

    
    