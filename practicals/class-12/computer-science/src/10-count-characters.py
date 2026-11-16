#: id: cs12-10
#: group: text-files
#: title: Read a text file and display the number of vowels, consonants, uppercase and lowercase characters in the file.
#: title_hi: एक टेक्स्ट फ़ाइल पढ़कर उसमें स्वरों, व्यंजनों, बड़े (uppercase) और छोटे (lowercase) अक्षरों की संख्या दिखाइए।
#: syllabus: yes
#: files: story.txt
# Program 10: Count vowels, consonants, uppercase and lowercase letters

vowels = consonants = upper = lower = 0
with open("story.txt", "r") as f:
    text = f.read()

for ch in text:
    if ch.isalpha():
        if ch.lower() in "aeiou":
            vowels += 1
        else:
            consonants += 1
        if ch.isupper():
            upper += 1
        else:
            lower += 1

print("Vowels     :", vowels)
print("Consonants :", consonants)
print("Uppercase  :", upper)
print("Lowercase  :", lower)
