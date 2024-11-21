


class SelectParser:
    
    def __init__(self):
        pass
    
    def get_node_parser(self, node_type: str):
        match node_type:
            case "Select":
                return self.parse_select
    
    def visit(self, node, *args, **kwargs):
        parser = self.get_node_parser(node.type)
        return parser(node, *args, **kwargs)   
    
    def parse_select(self, node):
        pass
    
    def parse_column_list_node(self, node):
        pass
    
    def parse_column_node(self, node):
        pass
    
    def parse_expression_node(self, node):
        pass
    
    def parse_expression_or_node(self, node):
        pass
    
    
    
    