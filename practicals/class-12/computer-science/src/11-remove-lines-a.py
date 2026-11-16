#: id: cs12-11
#: group: text-files
#: title: Remove all the lines that contain the character 'a' in a file and write them to another file.
#: title_hi: फ़ाइल की वे सभी पंक्तियाँ जिनमें 'a' अक्षर है, हटाकर दूसरी फ़ाइल में लिखिए।
#: syllabus: yes
#: files: school.txt
# Program 11: Move lines containing 'a' to another file

with open("school.txt", "r") as f:
    lines = f.readlines()

keep = []
moved = []
for line in lines:
    if "a" in line:
        moved.append(line)
    else:
        keep.append(line)

with open("school.txt", "w") as f:          # lines without 'a' stay
    f.writelines(keep)
with open("lines_with_a.txt", "w") as f:   # lines with 'a' go here
    f.writelines(moved)

print("Lines left in school.txt:")
with open("school.txt") as f:
    print(f.read(), end="")
print("\nLines written to lines_with_a.txt:")
with open("lines_with_a.txt") as f:
    print(f.read(), end="")
