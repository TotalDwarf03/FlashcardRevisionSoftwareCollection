#This script acts as a SQL Interface.
#Any database actions will happen here.

#Library Imports
from msilib.schema import Error
import sqlite3 as sql
from datetime import datetime as dt

class backgroundVars:
    """Contains variables used across the program"""
    database = r"DataStorage/cardsets.db"

def createConnection(dbFile):
    """Creates a connection to a database"""
    conn = None
    try:
        conn = sql.connect(dbFile) #Connect to database
        return conn
    except Error as e:
        print(e) #Error if can't connect
    return conn

def createTbl(conn, sqlCommand):
    """Executes the Command Given (Used when making the table)"""
    c = conn.cursor()
    c.execute(sqlCommand)
    conn.commit()

def setupTable():
    """Creates the Table in the database"""
    cardsetsTbl = """ CREATE TABLE IF NOT EXISTS flashcardsets (
                        id integer PRIMARY KEY AUTOINCREMENT,
                        setname text NOT NULL,
                        subject text NOT NULL,
                        datemodified text NOT NULL,
                        questions text NOT NULL,
                        answers text NOT NULL,
                        images text NOT NULL
                    );"""

    conn = createConnection(backgroundVars.database)
    
    #If database exists, create the flashcardSets table in it
    if conn is not None:
        createTbl(conn, cardsetsTbl) 
    else:
        print("Error")

def addData(conn, sql, data):
    """Executes the command Given (Used when inserting data)"""
    c = conn.cursor()
    c.execute(sql, data)
    conn.commit()

def insertData(data):
    """Inserts the given data into the table"""
    insert = """ INSERT INTO flashcardsets(setname, subject, datemodified, questions, answers, images)
                VALUES (?, ?, ?, ?, ?, ?);"""

    conn = createConnection(backgroundVars.database)
    with conn:
        addData(conn, insert, data)

def getAllData():
    """Returns all the data within the database"""
    conn = createConnection(backgroundVars.database)
    c = conn.cursor()
    sql = "SELECT * FROM flashcardsets;"
    data = c.execute(sql)
    sets = data.fetchall() #Gets Query data
    conn.commit()

    return sets

def getLastSetId():
    """Gets the most recent id from the database"""
    charsToRemove = "(,)"

    conn = createConnection(backgroundVars.database)
    c = conn.cursor()
    sql = "SELECT id FROM flashcardsets ORDER BY id DESC LIMIT 1;"

    try:
        data = c.execute(sql)
    except:
        value = None #If no database found, return None
    else:
        value = data.fetchone()

        #Removes ID formatting
        for char in charsToRemove:
            value = str(value).replace(char, "")

    conn.commit()
    return value

def renameSet(setId, setName, setSubject):
    """Updates the setName and subject fields"""

    #Gets date and time when function is called
    now = dt.now()
    dateModified = now.strftime("%d-%m-%Y %H:%M")

    conn = createConnection(backgroundVars.database)
    c = conn.cursor()
    sql = """UPDATE flashcardsets SET setname = ?, subject = ?, datemodified = ? WHERE id = ?;"""
    data = (setName, setSubject, dateModified, setId)

    c.execute(sql, data)
    conn.commit()

def deleteSet(setId):
    """Deletes a given set"""
    conn = createConnection(backgroundVars.database)
    c = conn.cursor()
    sql = """DELETE FROM flashcardsets WHERE id = ?;"""

    c.execute(sql, str(setId))
    conn.commit()

def fixIncrement():
    """Rearranges the ID's of each record in the database"""
    conn = createConnection(backgroundVars.database)
    c = conn.cursor()

    data = getAllData() #Get everything from table
    
    removeTblSql = """DROP TABLE flashcardsets"""
    c.execute(removeTblSql) #Delete the table

    for i in range(0, len(data)):
        data[i] = list(data[i])
        data[i].pop(0) #Remove setId from data for new one to be assigned

    setupTable() #Remake the table
    
    for i in data:
        insertData(i) #Inset data into table
    
    conn.commit()

def getRow(setId):
    """Gets the entire row of a given setID"""
    conn = createConnection(backgroundVars.database)
    c = conn.cursor()
    sql = """SELECT * FROM flashcardsets WHERE id = ?;"""

    row = c.execute(sql, str(setId)) #Get the given row
    flashcardSet = row.fetchone()   #Fetch the data
    flashcardSet = list(flashcardSet)
    return flashcardSet

def editSet(setId, data):
    """Updates flashcard set with the new information"""

    conn = createConnection(backgroundVars.database)
    c = conn.cursor()
    sql = """UPDATE flashcardsets SET setname = ?, subject = ?, datemodified = ?, questions = ?, answers = ?, images = ? WHERE id = ?;"""

    data.append(setId)

    c.execute(sql, data)
    conn.commit()