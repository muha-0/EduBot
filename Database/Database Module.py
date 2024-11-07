import sqlite3

sql_script = "Database/commands.sql"
db = "Database/edubot.db"


"""_summary_

init(database file path, SQL Script file path):
    connects to the database file and executes all transactions made to create tables, insert/update/delete instances,
    create indexes, etc.


write(database file path, SQL Script file path, command to make a transaction with):
    connects to the database file and execute any new transaction on the database, in case this transaction is new it will be
    appended to the SQL Script file
    
query(database file path, SQL Query)
    connects to the database file and execute SQL Queries on it then return the result as a list of tuples

"""
def init(db, sql_script):
    seesion = sqlite3.connect(db)
    cursor = seesion.cursor()
    
    with open(sql_script, 'r') as transactions:
        script = transactions.read()
        
        cursor.executescript(script)
        
    seesion.close()


    
def write(db, sql_script, command):
    session = sqlite3.connect(db, autocommit = True)
    cursor = session.cursor()
    
    cursor.execute(command)
    
    with open(sql_script, 'r') as commands_file:
        if((command + ';') in commands_file.read()):
            session.close()
            return
            
    
    with open(sql_script, 'a') as commands_file:
        commands_file.write(command + ';\n')
    
    session.close()
    
    
def query(db, SQLquery):
    session = sqlite3.connect(db)
    cursor = session.cursor()
    
    result = cursor.execute(SQLquery).fetchall()
    
    session.close()
    
    
    return result



# session = sqlite3.connect(db)
# cursor = session.cursor()

# print(cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall())
# # to get what tables are in the database at the moment

# print(query(db = db, SQLquery = "SELECT * FROM Employee e JOIN Job j ON e.job_id = j.job_id"))