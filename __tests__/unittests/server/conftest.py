import pytest

from dbcsv_server.query_engine.parser import Parser
from dbcsv_server.query_engine.printer import ASTPrinter
from dataclasses import dataclass

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

@pytest.fixture
def caller():
    @dataclass
    class Caller:
        data: any
        
    return Caller(data=dict(A=1))