import sqllite3
#connct to the database then check student db if not present create one
connection = sqllite3.connect('student.db')
#cursor object is used to execute aql cmds in py
cursor=connection.cursor()

#create the table
table_info="""
create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),
SECTION VARCHAR(25),MARKS INT);

"""
cursor.exeute(table_info)
#insert some records

cursor.execute('''INSERT INTO STUDENT VALUES('elli', 'gen ai', 'A', 99)''')
cursor.execute('''INSERT INTO STUDENT VALUES('james', 'computer science', 'B', 85)''')
cursor.execute('''INSERT INTO STUDENT VALUES('sara', 'mathematics', 'A', 92)''')
cursor.execute('''INSERT INTO STUDENT VALUES('mike', 'biology', 'C', 75)''')
cursor.execute('''INSERT INTO STUDENT VALUES('lisa', 'english', 'A+', 95)''')

#display the records
print('the records are')
data=cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)

#commit chnages to the db
connection.commit()
connection.close()