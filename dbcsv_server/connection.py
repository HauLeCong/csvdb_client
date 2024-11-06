from datetime import datetime, timezone
import uuid
import os
from pathlib import Path

class ConnectionIdentity:
    """
    Connection identity class, use to identify different connection
    """

    def __init__(self, folder_path: Path | str):
        self._id = uuid.uuid4()
        if isinstance(folder_path, Path) or isinstance(folder_path, str):
            self._folder_path = Path(folder_path) if isinstance(folder_path, str) else folder_path
            self.create_folder()
        else:
            raise TypeError("Folder path must be string or Path")
        self.closed = False
        self.query_result = {}
        self.created_at = datetime.now(tz=timezone.utc)

    @property
    def id(self) -> str:
        return self._id
    
    @property
    def folder_path(self):
        """
            A connection folder
        """
        return self._folder_path
                
    def create_folder(self):
        if not self._folder_path.exists() and not self._folder_path.is_dir():
            try:
                # Create folder
                self._folder_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                raise
                 
    @id.setter
    def id(self, id: str):
        """
        Set id for connection id
        Args:
            id (str): a random uuid
        """
        self._id = id

    def close(self):
        """
        Set status of connection to 0
        """
        self.closed = True
