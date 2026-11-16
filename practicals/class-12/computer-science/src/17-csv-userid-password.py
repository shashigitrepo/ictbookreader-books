#: id: cs12-17
#: group: csv-files
#: title: Create a CSV file by entering user-id and password, read it and search the password for a given user-id.
#: title_hi: user-id और password दर्ज करके एक CSV फ़ाइल बनाइए, उसे पढ़कर दिए गए user-id का password खोजिए।
#: syllabus: yes
#: inputs: 3 | riya01 | sun@123 | dev_k | Moon#45 | sam99 | star2024 | dev_k | alex
# Program 17: CSV file - search password for a user-id
import csv

n = int(input("How many users? "))
with open("users.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["userid", "password"])
    for i in range(n):
        uid = input("User-id : ")
        pwd = input("Password: ")
        writer.writerow([uid, pwd])

for i in range(2):
    search = input("\nEnter user-id to search: ")
    with open("users.csv", "r", newline="") as f:
        reader = csv.reader(f)
        next(reader)                         # skip the heading row
        for row in reader:
            if row[0] == search:
                print("Password is", row[1])
                break
        else:
            print("User-id not found")
