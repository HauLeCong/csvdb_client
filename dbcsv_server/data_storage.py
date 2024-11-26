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

    def create_table_file(
        self, con: ConnectionIdentity, database: str, table_name: str, cols_def: List
    ) -> Path:
        """
        Create a data file

        Args:
            con (ConnectionIdentity): current client connection
            database (str): database name
            table_name (str): table name
            cols_def (list): columns definition

        Raises:
            RuntimeError: when failed to create file

        Returns:
            Path: file location
        """
        file_folder = Path() / database
        # Check folder exists
        if not file_folder.exists():
            file_folder.mkdir(parents=True)
        df = pd.DataFrame(data=[], columns=[d["column_name"] for d in cols_def])
        meta_df = pd.DataFrame(data=cols_def)
        try:
            file_path = file_folder / f"{table_name}.csv"
            df.to_csv(file_path, index=False)
            meta_df.to_csv(file_folder / f"meta.{table_name}.csv", index=False)
        except Exception as e:
            raise RuntimeError(f"Unable to create table file {e}")
        finally:
            return file_path

    def select_file(
        self, con: ConnectionIdentity, database: str, table_name: str
    ) -> List[Dict]:
        """
        Return file content
        Args:
            con (ConnectionIdentity): connection
            database (str): database name
            table_name (str): table name

        Raises:
            FileNotFoundError: if data file not found

        Returns:
            List[Dict]
        """
        file_path = Path() / database / f"{table_name}.csv"
        if not file_path.is_file() or not file_path.exists():
            raise FileNotFoundError(f"Table {database}.{table_name} doest exists")
        df = pd.read_csv(file_path)
        return df.to_dict(orient="records")
