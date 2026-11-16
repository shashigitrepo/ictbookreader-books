#: id: cs12-29
#: group: python-sql
#: title: Write a Python program to connect to MySQL, create a database SCHOOL and a table STUDENT, and insert records entered by the user.
#: title_hi: MySQL से जुड़कर डेटाबेस SCHOOL और तालिका STUDENT बनाने तथा उपयोगकर्ता द्वारा दिए गए रिकॉर्ड डालने का पायथन प्रोग्राम लिखिए।
#: syllabus: yes
#: type: python-sql
#: reset: school
#: inputs: 3 | 1 | Aarav | Science | 86 | 2 | Diya | Commerce | 74 | 3 | Kabir | Science | 92
# Program 29: Create a database and table, and insert records
import mysql.connector as mycon

con = mycon.connect(host="localhost", user="root", passwd="tiger")
if con.is_connected():
    print("Connected to MySQL")
cur = con.cursor()
cur.execute("CREATE DATABASE IF NOT EXISTS school")
cur.execute("USE school")
cur.execute("""CREATE TABLE IF NOT EXISTS student (
                 rollno INT PRIMARY KEY,
                 name VARCHAR(20),
                 stream VARCHAR(12),
                 marks INT)""")
print("Database and table are ready")

n = int(input("How many records? "))
for i in range(n):
    roll = int(input("Roll number: "))
    name = input("Name       : ")
    stream = input("Stream     : ")
    marks = int(input("Marks      : "))
    query = "INSERT INTO student VALUES (%s, %s, %s, %s)"
    cur.execute(query, (roll, name, stream, marks))
con.commit()                       # save the changes permanently
print(n, "records inserted")
con.close()
