
from ..token import Token, ReservedWord
from typing import Dict
import re

class Scanner:
    """
        Scanner class to scan query string
    """
    def __init__(self, query_string):
        self.query_string = query_string
        self.token = []
        self.current_character = None
        self.iter_query_string = iter(query_string)
        self.current_line = 0
        self.current_position = 0
    
    def scan(self) -> Dict:
        pass
    
    
    def _next_character(self):
        try:
            self.current_character = next(self.iter_query_string)
        except StopIteration:
            raise
        
    def _scan_number_literal(self):
        """
            Scan number literal
        """       
        pass
    
    def _scan_string(self):
        """
            Scan identifier
        """
        pass
        
    def _scan_util(self, whole, reg_end):
        try:
            self._next_character()
            if reg_end.search(reg_end):
                return whole
            return self._scan_util(whole+self.current_character, reg_end)
        except:
            return whole
    
    