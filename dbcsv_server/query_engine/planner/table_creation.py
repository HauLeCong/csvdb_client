from ..ast_node import CreateTableNode
from .handler.create_table_handler import CreateTableHandler
class TableCreation:
    
    def __init__(self, node: CreateTableNode):
        self.create_table_node = node
        self.create_table_handler = CreateTableHandler(self)
        self.create_table_definition = self._get_handler_result(node)
        self.create_column_list = self._get_create_column_list()
        self.create_table_name = self._get_create_table_name()
        self.create_database = self._get_create_database()
        
    def _get_handler_result(self, node):
        return self.create_table_handler.handle(node)
    
    def _get_create_database(self):
        return self.create_table_definition["database"]
    
    def _get_create_column_list(self):
        return self.create_table_definition["definition"]
    
    def _get_create_table_name(self):
        return self.create_table_definition["table_name"]