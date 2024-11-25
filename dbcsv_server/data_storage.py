
import pandas as pd
from pathlib import Path
from typing import List, Dict
from .connection import ConnectionIdentity

class FileManager:
    """
        This class directly interact with server file system
    """
    def __init__(self):
        pass
    
    def create_table_file(self, con: ConnectionIdentity, database: str, table_name: str, cols_def: list) -> Path:
        file_folder = con.folder_path / database
        # Check folder exists
        if not file_folder.exists():
            file_folder.mkdir(parents = True, exist_ok= True)
        df = pd.DataFrame(data=[], columns=[d["column_name"] for d in cols_def])
        meta_df = pd.DataFrame(data=cols_def)
        try:
            file_path = file_folder/f"{table_name}.csv"
            df.to_csv(file_path, index=False)
            meta_df.to_csv(file_folder/f"meta.{table_name}.csv", index=False)
        except Exception as e:
            raise RuntimeError(f"Unable to create table file {e}")
        finally:
            return file_path 
    
    def select_file(self, con: ConnectionIdentity, database: str, table_name: str) -> pd.DataFrame:
        file_path = con.folder_path / database / f"{table_name}.csv"
        if not file_path.is_file() or not file_path.exists():
            raise FileNotFoundError(f"Table {table_name} doest exists")
        df = pd.read_csv(file_path)
        return df.to_dict(orient="records")
    
        
    
