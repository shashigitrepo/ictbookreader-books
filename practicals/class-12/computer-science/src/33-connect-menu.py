#: id: cs12-33
#: group: python-sql
#: title: Write a menu-driven Python–MySQL program to add a student, show all students, and show the students of a given stream with marks above a given value.
#: title_hi: विद्यार्थी जोड़ने, सभी विद्यार्थी दिखाने तथा दी गई स्ट्रीम में दिए गए अंकों से अधिक वाले विद्यार्थी दिखाने का मेनू-आधारित पायथन–MySQL प्रोग्राम लिखिए।
#: type: python-sql
#: setup: connect-setup.sql
#: inputs: 1 | 5 | Rohan | Science | 81 | 2 | 3 | Science | 85 | 4
# Program 33: Menu-driven student database
import mysql.connector as mycon

con = mycon.connect(host="localhost", user="root", passwd="tiger", database="school")
cur = con.cursor()


def add_student():
    data = (int(input("Roll number: ")), input("Name       : "),
            input("Stream     : "), int(input("Marks      : ")))
    cur.execute("INSERT INTO student VALUES (%s, %s, %s, %s)", data)
    con.commit()
    print("Student added")


def show_all():
    cur.execute("SELECT * FROM student")
    for row in cur.fetchall():
        print(*row, sep="\t")


def show_stream():
    stream = input("Stream     : ")
    limit = int(input("Marks above: "))
    cur.execute("SELECT name, marks FROM student WHERE stream = %s AND marks > %s", (stream, limit))
    rows = cur.fetchall()
    if rows:
        for name, marks in rows:
            print(name, marks)
    else:
        print("No student found")


while True:
    print("\n1. Add student  2. Show all  3. Search by stream  4. Exit")
    choice = input("Choice: ")
    if choice == "1":
        add_student()
    elif choice == "2":
        show_all()
    elif choice == "3":
        show_stream()
    elif choice == "4":
        print("Bye")
        break
con.close()
