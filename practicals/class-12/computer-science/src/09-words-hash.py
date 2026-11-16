#: id: cs12-09
#: group: text-files
#: title: Read a text file line by line and display each word separated by a #.
#: title_hi: एक टेक्स्ट फ़ाइल को पंक्ति-दर-पंक्ति पढ़कर प्रत्येक शब्द को # से अलग करके दिखाइए।
#: syllabus: yes
#: files: story.txt
# Program 9: Display words of a text file separated by #

with open("story.txt", "r") as f:
    for line in f:
        words = line.split()
        print("#".join(words))
