
from typing import Union, Literal, Optional
from dataclasses import dataclass

from .visitor import ASTHandler

ComparisionOperator = Literal[">", "<", "=", "<>"]
AddtionOperator = Literal["+", "-"]
FactorOperator = Literal["*", "/"]

@dataclass
class AST:
    """
        `<root>` :: = `<select>` | `<create>`  
    """
    nodes: Union["SelectNode", "CreateTableNode"]

@dataclass
class SelectNode:
    """
        `<select>` :: = 'SELECT' `<column_list>` 'FROM' `<from_clause>` 'WHERE' `<where_clause>`
    """
    type = "Select"
    column_list: "ColumnListNode"
    from_clause: "FromNode"
    where_clause: "WhereNode"
      
@dataclass
class CreateTableNode:
    """
        `<create_table>` ::= CREATE TABLE `<table_name>` `<table_element_list>`
    """
    type = "Create"
    table_name: "IdentifierNode"
    table_element_list: "TableElementListNode"
    
@dataclass
class WhereNode:
    """
        `<where_clause>` ::= `<logical>` | `<where_clause>`
    """
    type = "Where"
    expr: Union["LogicalNode", "WhereNode"]
    
@dataclass
class FromNode:
    """
        `<from_clause>` ::= `<identifier>`
    """
    type =  "From"
    expr: "IdentifierNode"
    
@dataclass
class ColumnListNode:
    """
        `<column_list>` :: = `<column_list>`, `<column>` | `<column>`
    """
    type = "ColumnList"
    left: Union["ColumnNode","ColumnListNode"]
    right: "ColumnNode"
    operator: Literal[","] = None

@dataclass
class ColumnNode:
    """
        `<column>` :: = `<column_wild_card>` | `<column_name>` [AS `<alias>::= <str>`] | `<expr>`
    """
    type =  "Column"
    expr: Union["ExprNode", "ColumnWildCardNode", "ColumnNameNode"]
    alias: Optional[str] = None
    
@dataclass
class ColumnWildCardNode:
    """
        `<column_wild_card>` ::= "*"
    """
    type = "ColumnWildCard"
    values = "*"
    
@dataclass
class ColumnNameNode:
    """
        `<column_name>` ::= `<identifier>`
    """
    type = "ColumnName"
    expr: "IdentifierNode"

@dataclass
class TableElementListNode:
    """
        `<table_element_list>` ::= "(" `<table_element>`[{"," `<table_element>`}] ")"
    """
    type = "TableElementList"
    expr: "TableElementNode"
    
@dataclass
class TableElementNode:
    """
        `<table_element>` ::= `<identifier>`
    """
    type = "TableElement"
    expr: "IdentifierNode"
    
@dataclass
class ExprNode:
    """
        `<expr>` :: =  `<arimethic_node>` | `<logical_node>` | `<comparison_node>`
    """
    type = "Expr"
    expr: Union["ArimethicNode", "LogicalNode", "ComparisionNode"]

@dataclass
class IdentifierNode:
    """
        `<indentifier>` :: = `<str>`
    """
    type = "Indentifier"
    value: str
    
@dataclass
class LogicalNode:
    """
        `<logical>` ::= `<logical_term>` | `<logical_node>` 'OR' `<logical_term>`
    """
    left: Union["LogicalTermNode", "LogicalNode"]
    right: "LogicalTermNode"
    operator: Optional[Literal["OR"]]
    
@dataclass
class LogicalTermNode:
    """
        `<logical_term>` ::= `<logical_factor>` | `<logical_term>` AND `<logical_factor>` 
    """
    left: Union["LogicalFactorNode", "LogicalTermNode"]
    right: "LogicalFactorNode"
    operator: Optional[Literal["AND"]]

@dataclass
class LogicalFactorNode:
    """
        `<logical_factor>` ::= ["NOT"] `<literal_boolean>` 
    """
    expr: "LiteralBoolean"
    operator: Optional[Literal["NOT"]]

@dataclass
class ArimethicNode:
    """
        `<arimethic>` :: = `<term>`
        | `<arimethic>` "+" `<term>`
        | `<arimethic>` "-" `<term>`
    """
    type = "Arimethic"
    left: Union["TermNode", "ArimethicNode"]
    right: "TermNode"
    operator: Optional["AddtionOperator"]
    
    def value(self, handler: ASTHandler):
        return handler.visit(self)
    
@dataclass
class TermNode:
    """
        `<term>` :: = `<factor>`
        | `<term>` "*" `<factor>`
        | `<term> "/" <factor>`
    """
    type = "Term"
    left: Union["FactorNode", "TermNode"]
    right: Optional["FactorNode"]
    operator: Optional["FactorOperator"]

@dataclass
class FactorNode:
    """
        `<factor>` :: = ["+"]`<literal_number>` | ["-"]`<literal_number>` | (<arimethic>)
    """
    type = "Factor"
    expr: Union["LiteralNumber", "ArimethicNode"]
    
@dataclass
class ComparisionNode:
    pass
   
@dataclass
class LiteralNumber:
    """
        `<literal_number>`:: = int
    """
    type = "LiteralNumber"
    value: int
    
@dataclass
class LiteralString:
    """
        `<literal_string>` :: = str
    """
    type = "Literal String"
    value: str
    
@dataclass 
class LiteralBoolean:
    """
        `<literal_boolean>` :: = boolean
    """
    type = "Boolean"
    value: bool