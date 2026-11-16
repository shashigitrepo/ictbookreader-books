#: id: cs12-14
#: group: binary-files
#: title: Create a binary file with name and roll number. Search for a given roll number and display the name; if not found, display an appropriate message.
#: title_hi: नाम और रोल नंबर वाली एक बाइनरी फ़ाइल बनाइए। दिए गए रोल नंबर को खोजकर नाम दिखाइए; न मिलने पर उचित संदेश दिखाइए।
#: syllabus: yes
#: inputs: 3 | 101 | Aarav Sharma | 102 | Meera Singh | 103 | Kabir Khan | 102 | 110
# Program 14: Binary file - search a roll number
import pickle

n = int(input("How many students? "))
with open("students.dat", "wb") as f:
    for i in range(n):
        roll = int(input("Roll number: "))
        name = input("Name       : ")
        pickle.dump([roll, name], f)
print("Records saved in students.dat")


def search(roll_no):
    with open("students.dat", "rb") as f:
        try:
            while True:
                record = pickle.load(f)
                if record[0] == roll_no:
                    return record[1]
        except EOFError:          # end of file reached
            return None


for i in range(2):
    r = int(input("\nEnter roll number to search: "))
    name = search(r)
    if name:
        print("Name of roll number", r, "is", name)
    else:
        print("Roll number", r, "not found")
