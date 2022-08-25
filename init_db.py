import sqlite3

connection = sqlite3.connect('selftestcovid19.db')
with open('selftestcovid19.sql') as f:
    connection.executescript(f.read())
connection.commit()
connection.close()