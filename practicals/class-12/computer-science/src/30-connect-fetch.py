#: id: cs12-30
#: group: python-sql
#: title: Write a Python program to display all the records of the STUDENT table using fetchall(), the first record using fetchone(), and the number of records using rowcount.
#: title_hi: STUDENT तालिका के सभी रिकॉर्ड fetchall() से, पहला रिकॉर्ड fetchone() से और रिकॉर्ड की संख्या rowcount से दिखाने का पायथन प्रोग्राम लिखिए।
#: syllabus: yes
#: type: python-sql
#: setup: connect-setup.sql
# Program 30: fetchall(), fetchone() and rowcount
import mysql.connector as mycon

con = mycon.connect(host="localhost", user="root", passwd="tiger", database="school")
cur = con.cursor()

cur.execute("SELECT * FROM student")
rows = cur.fetchall()
print("All records (fetchall):")
print("%-8s%-10s%-12s%s" % ("Roll", "Name", "Stream", "Marks"))
for row in rows:
    print("%-8s%-10s%-12s%s" % row)
print("Number of records (rowcount):", cur.rowcount)

cur.execute("SELECT * FROM student ORDER BY marks DESC")
top = cur.fetchone()               # only the first row of the result
print("\nTopper (fetchone):", top)
cur.fetchall()                     # read the remaining rows before the next query
con.close()
