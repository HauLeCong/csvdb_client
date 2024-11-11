import pytest

from dbcsv_server.query_engine import QueryParser

class MocKQueryParser:
    
    @staticmethod
    def parse(parser):
        parser.iter_token = iter(parser.token)
        parser.advance_token()
        

@pytest.fixture
def mock_parser(request):
    _parser = QueryParser(request.param)
    MocKQueryParser.parse(_parser)
    return _parser