
import dbcsv
import sqlite3

con = dbcsv.connect('abc')
cursor = con.cursor()
assert cursor.execute("selec 1", None)

con = sqlite3.connect()