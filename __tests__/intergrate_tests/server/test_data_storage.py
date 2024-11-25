from dbcsv_server.connection import ConnectionIdentity
from dbcsv_server.db_controller import DBController
from dbcsv_server.data_storage import FileManager
from dbcsv_server.query_engine.parser import Parser
from dbcsv_server.query_engine.planner.table_creation import TableCreation
from pathlib import Path
import pytest

@pytest.mark.parametrize("valid_query", ["CREATE TABLE A.T (col1 STRING, col2 STRING, col3 INT)"])
def test_create_file_on_create_query(valid_query):
    con = ConnectionIdentity(Path("data/storage"))
    file_manager = FileManager()
    parser = Parser(valid_query)
    ast_nodes = parser.parse()
    table_creation = TableCreation(ast_nodes.nodes)
    database = table_creation.get_create_database()
    columns_definition = table_creation.get_create_column_list()
    table_name = table_creation.get_create_table_name()
    assert table_name == "T"
    assert columns_definition == [{"column_name": "COL1", "column_type": "STRING"}, {"column_name": "COL2", "column_type": "STRING"}, {"column_name": "COL3", "column_type":"INT"}]
    result_file = file_manager.create_table_file(con, database, table_name, columns_definition)
    assert result_file.exists()
    data_select = file_manager.select_file(con, database, table_name)