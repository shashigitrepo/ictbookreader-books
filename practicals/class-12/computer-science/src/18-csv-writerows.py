#: id: cs12-18
#: group: csv-files
#: title: Write the records of books (book id, title, price) to a CSV file using writerows(), then read the file and display the books costing more than 300.
#: title_hi: writerows() से पुस्तकों के रिकॉर्ड (book id, title, price) CSV फ़ाइल में लिखिए, फिर फ़ाइल पढ़कर 300 से महँगी पुस्तकें दिखाइए।
# Program 18: CSV file - writerows() and reader()
import csv

books = [
    ["B101", "Python Basics", 350],
    ["B102", "Data Structures", 280],
    ["B103", "Computer Networks", 420],
    ["B104", "SQL in Practice", 300],
]

with open("books.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["bookid", "title", "price"])
    w.writerows(books)

print("Books costing more than 300:")
with open("books.csv", "r", newline="") as f:
    r = csv.reader(f)
    header = next(r)
    count = 0
    for row in r:
        if int(row[2]) > 300:
            print(row[0], row[1], row[2], sep=" | ")
            count += 1
print("Total:", count)
