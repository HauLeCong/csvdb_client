import pytest

from dbcsv_server.query_engine.parser import Parser
from dbcsv_server.query_engine.visitor import ASTPrinter

class MocKQueryParser:
    
    @staticmethod
    def parse(parser):
        parser.iter_token = iter(parser.token)
        parser.advance_token()
        

@pytest.fixture
def mock_parser(request):
    _parser = Parser(request.param)
    MocKQueryParser.parse(_parser)
    return _parser

@pytest.fixture
def ast_printer():
    return ASTPrinter()