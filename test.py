from dbcsv_server.query_engine import QueryParser

parser = QueryParser("abc~")
parser.scan()
print(parser.token)