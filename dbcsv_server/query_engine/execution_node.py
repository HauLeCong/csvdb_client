from dataclasses import dataclass
from typing import Union, List

"""
    Plan node or execution node order
    Is a tree like AST, each Node from AST will convert into a plan 
    This plan mimic realtional algebra - in csvdb only 3 operation is support SELECT, GET, PROJECT
"""
@dataclass
class ProjectExecNode:
    """SQL equivalence: `<Select clause>`"""
    type = "Project"
    child: Union["SelectExecNode", "ProjectExecNode"]
    projects: List
    
@dataclass
class SelectExecNode:
    """SQL equivalance: `<Where clause>`"""
    type = "Select"
    child: Union["ScanExecNode", "ProjectExecNode"]
    predicate: str

@dataclass
class ScanExecNode:
    """SQL equivalence: `<From clause>`"""
    type = "Scan"
    table: str
    
    