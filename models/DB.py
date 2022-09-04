import sqlite3

def initDB():
    connection = sqlite3.connect('./models/selftestcovid19.db')
    with open('./models/selftestcovid19.sql') as f:
        connection.executescript(f.read())
    connection.commit()
    connection.close()

def connectDB():
    connection = sqlite3.connect('./models/selftestcovid19.db')
    connection.row_factory = sqlite3.Row
    return connection