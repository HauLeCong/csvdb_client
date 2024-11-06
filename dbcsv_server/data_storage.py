
import pandas as pd
from pathlib import Path
from .connection import ConnectionIdentity

class FileManager:
    """
        This class directly interact with server file system
    """
    def __init__(self):
        pass
    
    def create_file(con: ConnectionIdentity, file_name: str, cols: list) -> None:
        file_folder = con.folder_path / con.id / file_name
        # Check folder exists
        if not file_folder.exists() and not file_folder.isdir():
            file_folder.mkdir(parents = True, exists_ok = True)
        df = pd.DataFrame(data=[], columns=cols)
        df.to_csv(file_folder, index=False)
    
    def select_file(con: ConnectionIdentity, file_name: str) -> dict:
        file_folder = con.folder_path / con.id / file_name
        if not file_folder.is_file():
            raise FileNotFoundError("File name doest exists")
        df = pd.read_csv(file_folder)
        return df.to_dict()
        
    
