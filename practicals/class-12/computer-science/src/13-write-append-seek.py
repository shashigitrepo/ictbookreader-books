#: id: cs12-13
#: group: text-files
#: title: Write lines to a text file using write() and writelines(), append a line, and use seek() and tell() while reading it.
#: title_hi: write() और writelines() से टेक्स्ट फ़ाइल में पंक्तियाँ लिखिए, एक पंक्ति जोड़िए (append) और पढ़ते समय seek() व tell() का उपयोग कीजिए।
# Program 13: write(), writelines(), append mode, seek() and tell()

with open("notes.txt", "w") as f:
    f.write("Python is easy to learn.\n")
    f.writelines(["Files store data permanently.\n", "Text files store characters.\n"])

with open("notes.txt", "a") as f:
    f.write("This line was appended.\n")

with open("notes.txt", "r") as f:
    print("Position at start   :", f.tell())
    first = f.readline()
    print("First line          :", first, end="")
    print("Position after line :", f.tell())
    f.seek(10)                      # jump to the 11th character
    print("Read 14 characters from position 10:", f.read(14))
    f.seek(0)                       # back to the beginning
    print("All lines with readlines():")
    for line in f.readlines():
        print("  ", line, end="")
