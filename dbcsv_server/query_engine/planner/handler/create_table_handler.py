
from .base_handler import BaseHandler
from ...ast_node import (
    CreateTableNode,
    TableDefinitionGroupNode,
    TableDefinitionListNode,
    TableDefinitionNode,
    ColumnDefinitionNode
)

class CreateTableHandler(BaseHandler):
    def __init__(self, caller):
        super().__init__(caller)
        self.holding_left = []
        self.holding_right = []
        
    def call_handler(self, node, *args, **kwargs):
        
        handler = self.get_node_handler(node.type)
        return handler(node, *args, **kwargs)
    
    def get_node_handler(self, node_type: str):
        match node_type:
            case "Create":
                return self.handle
            case "TableDefinitionGroup":
                return self.handle_table_definition_group_node
            case "TableDefinitionList":
                return self.handle_table_definition_list_node
            case "TableDefinitionNode":
                return self.handle_table_definition_node
            case "ColumnDefinition":
                return self.handle_column_definition_node
            case _:
                raise RuntimeError(f"Unsupport handling {node_type}")
    
    def handle(self, node: CreateTableNode):
        print("***Call this")
        table_definition_group = self.call_handler(node.table_definition_group)
        return dict(table_name = node.table_name.expr[1], definition = table_definition_group)
    
    def handle_table_definition_group_node(self, node: TableDefinitionGroupNode):
        return self.call_handler(node.table_definition_list)
    
    def handle_table_definition_list_node(self, node: TableDefinitionListNode):
        if isinstance(node.left, TableDefinitionListNode):
            self.call_handler(node.left)
            if node.right:
                right_value = self.call_handler(node.right)
                self.holding_right.append(right_value)
                print(self.holding_right)
        else:
            left_value = self.call_handler(node.left)
            self.holding_left.append(left_value)
            print(left_value)
        return self.holding_left + self.holding_right
    
    def handle_table_definition_node(self, node: TableDefinitionNode):
        return dict(column_name = node.column_name[1], column_type = self.call_handler(node.column_definition))
    
    def handle_column_definition_node(self, node: ColumnDefinitionNode):
        return node.type_name[0].value