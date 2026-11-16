#: id: cs12-15
#: group: binary-files
#: title: Create a binary file with roll number, name and marks. Input a roll number and update the marks.
#: title_hi: रोल नंबर, नाम और अंकों वाली बाइनरी फ़ाइल बनाइए। रोल नंबर लेकर उसके अंक अपडेट कीजिए।
#: syllabus: yes
#: inputs: 2 | 88
# Program 15: Binary file - update marks
import pickle

records = [[1, "Ananya", 78], [2, "Rohan", 65], [3, "Ishita", 91]]
with open("result.dat", "wb") as f:
    pickle.dump(records, f)          # the whole list is stored as one object


def show():
    with open("result.dat", "rb") as f:
        for roll, name, marks in pickle.load(f):
            print(f"{roll:<5}{name:<10}{marks}")


print("Before update:")
show()

roll = int(input("\nEnter roll number to update: "))
with open("result.dat", "rb") as f:
    data = pickle.load(f)

found = False
for rec in data:
    if rec[0] == roll:
        rec[2] = int(input("Enter new marks: "))
        found = True

if found:
    with open("result.dat", "wb") as f:
        pickle.dump(data, f)
    print("Marks updated.\n\nAfter update:")
    show()
else:
    print("Roll number not found")
