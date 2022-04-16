import sqlite3 as sql

#creates a conection to the database with a cursor to apply method to it
conn = sql.connect("fitbitData.db")
c = conn.cursor()

#data set to be stored
data = [["john", "01-02-2021", "20:00", "upload", 7500, 88], ["john", "02-02-2021", "20:00", "upload", 9000, 86], ["john", "03-02-2021", "20:00", "upload", 7800, 90],
        ["john", "04-02-2021", "20:00", "upload", 8000, 86], ["john", "05-02-2021", "20:00", "upload", 8500, 88]]
data2 = [["charlie", "01-02-2021", "20:00", "upload", 4000, 123], ["charlie", "02-02-2021", "20:00", "upload", 4500, 92], ["charlie", "03-02-2021", "20:00", "upload", 7000, 90],
        ["charlie", "04-02-2021", "20:00", "upload", 5000, 95], ["charlie", "05-02-2021", "20:00", "upload", 4250, 88]]

#Creates table
c.execute("""CREATE TABLE data
            (user, date, time, status, steps, heartRate)""")

#Inserts example data
c.executemany("INSERT INTO data VALUES (?, ?, ?, ?, ?, ?)", data)
c.executemany("INSERT INTO data VALUES (?, ?, ?, ?, ?, ?)", data2)

for row in c.execute("SELECT * FROM data"):
    print(row)

#Save changes
conn.commit()

#Closes Connection
conn.close()