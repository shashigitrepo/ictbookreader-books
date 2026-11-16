#: id: cs12-08
#: group: exceptions
#: title: Write a program that reads an index and shows the element of a list, handling IndexError and ValueError, with an else block that runs when no error occurs.
#: title_hi: सूची के किसी इंडेक्स का तत्व दिखाने का प्रोग्राम लिखिए जिसमें IndexError व ValueError संभाले जाएँ और त्रुटि न होने पर else ब्लॉक चले।
#: inputs: 2 | 7 | two
# Program 8: try-except-else with IndexError and ValueError

subjects = ["English", "Physics", "Chemistry", "Maths", "Computer Science"]

for i in range(3):
    try:
        pos = int(input("Enter an index (0 to 4): "))
        name = subjects[pos]
    except IndexError:
        print("IndexError: there is no subject at that index.")
    except ValueError:
        print("ValueError: the index must be a number.")
    else:
        print("Subject at index", pos, "is", name)
