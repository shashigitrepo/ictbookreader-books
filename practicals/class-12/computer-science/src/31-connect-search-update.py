#: id: cs12-31
#: group: python-sql
#: title: Write a Python program to search a student by roll number and update the marks, using the format() method in the query.
#: title_hi: रोल नंबर से विद्यार्थी को खोजने और उसके अंक अपडेट करने का पायथन प्रोग्राम लिखिए, जिसमें क्वेरी में format() विधि का उपयोग हो।
#: syllabus: yes
#: type: python-sql
#: setup: connect-setup.sql
#: inputs: 2 | 79 | 9
# Program 31: Search and update a record using format()
import mysql.connector as mycon

con = mycon.connect(host="localhost", user="root", passwd="tiger", database="school")
cur = con.cursor()

for i in range(2):
    roll = int(input("\nEnter roll number: "))
    cur.execute("SELECT * FROM student WHERE rollno = {}".format(roll))
    rec = cur.fetchone()
    if rec is None:
        print("No student with roll number", roll)
        continue
    print("Found:", rec)
    new_marks = int(input("Enter new marks: "))
    cur.execute("UPDATE student SET marks = {} WHERE rollno = {}".format(new_marks, roll))
    con.commit()
    print(cur.rowcount, "record updated")
    cur.execute("SELECT * FROM student WHERE rollno = {}".format(roll))
    print("Now:", cur.fetchone())
con.close()
