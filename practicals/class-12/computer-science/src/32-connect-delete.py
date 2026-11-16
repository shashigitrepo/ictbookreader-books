#: id: cs12-32
#: group: python-sql
#: title: Write a Python program to delete the record of a student whose roll number is entered by the user (using the %s format specifier), and display the remaining records.
#: title_hi: उपयोगकर्ता द्वारा दिए गए रोल नंबर वाले विद्यार्थी का रिकॉर्ड हटाने (%s फ़ॉर्मेट स्पेसिफ़ायर से) और बचे हुए रिकॉर्ड दिखाने का पायथन प्रोग्राम लिखिए।
#: syllabus: yes
#: type: python-sql
#: setup: connect-setup.sql
#: inputs: 4
# Program 32: Delete a record using %s
import mysql.connector as mycon

con = mycon.connect(host="localhost", user="root", passwd="tiger", database="school")
cur = con.cursor()

roll = int(input("Enter roll number to delete: "))
cur.execute("DELETE FROM student WHERE rollno = %s", (roll,))
con.commit()
if cur.rowcount == 0:
    print("No such record")
else:
    print("Record deleted")

cur.execute("SELECT rollno, name, marks FROM student")
print("Remaining records:")
for r in cur.fetchall():
    print(r[0], r[1], r[2])
con.close()
