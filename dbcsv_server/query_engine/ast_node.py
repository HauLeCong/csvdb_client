
from typing import Union, Literal, Optional
from dataclasses import dataclass


ComparisionOperator = Literal[">", "<", "=", "<>", ">=", "<="]
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
        `<select>` :: = 'SELECT' `<column_list>` `<from_clause>` `<where_clause>`
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
        `<where_clause>` ::= WHERE `<predicate>`
    """
    type = "Where"
    expr: Union["PredicateNode"]
    
@dataclass
class FromNode:
    """
        `<from_clause>` ::= FROM `<source>`
    """
    type =  "From"
    expr: "IdentifierNode"
    
@dataclass
class Source:
    """
        `<source>` ::= `<source_list>`
    """
    type = "Source"
    expr: "SourceListNode"
        
@dataclass
class SourceListNode:
    """
        `<source_list>` ::= `<source_list>`.`<source_name>` | `<source_name>`
    """
    type = "SourceList"
    left: Union["SourceListNode", "SourceNameNode"]
    right: "SourceNameNode"
    
@dataclass
class SourceNameNode:
    """
        `<schema_name>` ::= `<identifier>`
    """
    type = "SourceName"
    expr: "IdentifierNode"
 
    
@dataclass
class ColumnListNode:
    """
        `<column_list>` :: = `<column_list>`, `<column>` | `<column>`
    """
    type = "ColumnList"
    left: Union["ColumnNode","ColumnListNode"]
    right: "ColumnNode"
    operator: Optional[Literal[","]]

@dataclass
class ColumnNode:
    """
        `<column>` :: = `<column_wild_card>` | \n
        `<expr>` AS `<alias>` | \n
        `<expr>` `<alias>` | \n
        `<alias>` = `<expr>` | \n
        `<expr>`
    """
    type =  "Column"
    expr: Union["ExprNode", "ColumnWildCardNode"]
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
class PredicateNode:
    """
        `<predicate>` ::= `<predicate_or>`
    """
    type = "Predicate"
    expr: "PredicateOrNode"
    
@dataclass
class PredicateOrNode:
    """
        `<predicate_or>` ::= `<predicate_or>` OR `<predicate_and>` | `<predicate_or>`
    """
    type = "PredicateOr"
    left: Union["PredicateOrNode", "PredicateAndNode"]
    right: "PredicateAndNode"
    operator: Optional[Literal["OR"]]
    
@dataclass
class PredicateAndNode:
    """
        `<predicate_and>` ::= `<predicate_and>` AND `<predicate_not>` | `<predicate_not>`
    """
    type = "PredicateAnd"
    left: Union["PredicateAndNode", "PredicateNotNode"]
    right: "PredicateNotNode"
    operator: Optional[Literal["AND"]]
 
@dataclass
class PredicateNotNode:
    """
        `<predicate_not>` ::= NOT `<predicate_compare>` | `<predicate_compare>`
    """
    type = "PredicateNot"
    expr: "PredicateCompareNode"
    operator: Optional[Literal["NOT"]]
    
@dataclass
class PredicateCompareNode:
    """
        `<predicate_compare>` ::=
            `<expression>` =  `<expression>` | \n
            `<expression>` >= `<expression>` | \n
            `<expression>` <= `<expression>` | \n
            `<expression>` >  `<expression>` | \n
            `<expression>` <  `<expression>` | \n
            `<expression>` <> `<expression>` | \n
            `<predicate_parent>`
    """
    type = "PredicateCompare"
    left: Union["ExprNode", "PredicateParentNode"]
    right: "ExprNode"
    operator: Optional[ComparisionOperator]
    
@dataclass
class PredicateParentNode:
    """
        `<predicate_parent>` ::= `(<predicate>)`
    """
    type = "PredicateParent"
    expr: "PredicateNode"

@dataclass
class ExprNode:
    """
        `<expr>` ::=  `<expr_add>`
    """
    type = "Expr"
    expr: Union["ExprAddNode"]

@dataclass
class ExprAddNode:
    """
        `<expr_add>` ::= `<expr_add>` + `<expr_multi>` | \n
        `<expr_add>` - `<expr_multi>` | \n
        `<expr_multi>` 
    """
    type = "ExprAdd"
    left: Union["ExprAddNode", "ExprMultiNode"]
    right: "ExprMultiNode"
    operator: Optional[AddtionOperator]

@dataclass
class ExprMultiNode:
    """
        `<expr_mulit>` ::= `<expr_multi>` * `<expr_value>` |\n
        `<expr_multi>` / `<expr_value>` |\n
        `<expr_multi>` % `<expr_value>` |\n
        `<expr_value>`
    """
    type = "ExprMulti"
    left: Union["ExprMultiNode", "ExprValueNode"]
    right: "ExprValueNode"
    operator: Optional[FactorOperator]
    
    
@dataclass
class ExprValueNode:
    """
        <expr_value> ::= `<literal>` | `<value>`
    """
    type = "ExprValue"
    expr: Union["ValueNode", "LiteralNode", ]
    
@dataclass
class ValueNode:
    """
        `<value>` ::=  `<identifier>` | `<expr_parent>`
    """
    type = "Value"
    expr: Union["IdentifierNode", "ExprParentNode"]
    
@dataclass
class ExprParentNode:
    """
        `<expr_parent>` ::= (`<expr>`)
    """
    type = "ExprParent"
    expr: "ExprNode"
    
@dataclass
class LiteralNode:
    """
        `<literal>` ::= <digit> | <string>
    """
    type = "Literal"
    expr: Union[str, float, int]
    

@dataclass
class IdentifierNode:
    """
        `<indentifier>` :: = `<str>`
    """
    type = "Indentifier"
    value: str 
   
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