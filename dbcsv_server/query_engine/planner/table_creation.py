from ..ast_node import CreateTableNode
from ...data_storage import FileManager

class TableCreation:
    
    def __init__(self, create_table_node: CreateTableNode):
        self.creat_table_node = create_table_node
        
    def file_create(self):
        pass
    
    def metadata_create(self):
        pass