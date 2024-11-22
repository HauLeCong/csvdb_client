


"""
    <schema_list> ::= <schema_list>.<schema_name>. | <schema_name>
    
    <schema_name>
    <schema_name>.<schema_name>.
    
    <source> ::= <schema_list>.<file_name>
    <schema_list> = <schema_list>.<schema_name> | <schema_name> |
    
    <schema_list>::= <schema_name>.<schema_list> | <schema_name>. |
    
    None
    schema_name.
    schema_name.schema_name.
    schema_name.schema_name.schema_name
    

""" 

