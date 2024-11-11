from dbcsv_server.query_engine import QueryParser

parser = QueryParser("abc~")
parser.scan()
print(parser.token)

class ASTPrinter:
    
    def get_handler(self, node_type) -> ASTHandler:
        pass
    
    def visit(self, node):
        handler = self.get_handler(node)
        return handler(node)
        
    def handle_logical_node(self, logical_node):
        #left, right, operator
        left_value = self.visit(logical_node.left)
        right_value = self.visit(logical_node.right)
        if logical_node.operator == "AND":
            return left_value and right_value