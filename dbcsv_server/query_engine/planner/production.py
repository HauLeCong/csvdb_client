from typing import List, Dict

from ..ast_node import FromNode
from ...data_storage import FileManager
from .handler import column_list_handler


class Production:
    
    def __init__(self, node: FromNode, source_func):
        self.source_func = source_func
        self.production_node = node
        self._get_data_source()
        self.current_index = 0
        self.current_row = None
        
    
    def __iter__(self):
        return self
    
    def _get_data_source(self) -> List[Dict]:
        database = self.production_node.database.expr[1]
        table_name = self.production_node.table_name.expr[1]
        try:
            self.source = self.source_func(database=database, table_name = table_name)
            self.meta = self.source_func(database=database, table_name = f"meta.{table_name}")
            self.source_length = len(self.source)
        except Exception as e:
            raise e
        
    def _apply_metadata(self, result_row) -> List[Dict]:
        for r in self.meta:
            match r["column_type"]:
                case "STRING":
                    result_row[r["column_name"]] = str(result_row[r["column_name"]])
                case "INT":
                    result_row[r["column_name"]] = int(result_row[r["column_name"]])
                case "FLOAT":
                    result_row[r["column_name"]] = float(result_row[r["column_name"]])
                case _:
                    raise RuntimeError(f'Unsupport type {r["column_type"]}')
        return result_row
        
    def __next__(self) -> Dict:
        if self.current_index < self.source_length:
            current_row = self.source[self.current_index]
            current_row_typed = self._apply_metadata(current_row)
            self.current_index += 1
            return current_row_typed
        raise StopIteration
            
            
    