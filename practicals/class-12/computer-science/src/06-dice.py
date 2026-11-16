#: id: cs12-06
#: group: functions
#: title: Write a random number generator that generates random numbers between 1 and 6 (simulates a dice).
#: title_hi: एक रैंडम संख्या जनरेटर लिखिए जो 1 और 6 के बीच रैंडम संख्याएँ बनाए (पासे का अनुकरण)।
#: syllabus: yes
#: inputs: y | y | y | n
# Program 6: Dice simulator using the random module
import random


def roll_dice():
    return random.randint(1, 6)


rolls = 0
while True:
    answer = input("Roll the dice? (y/n): ")
    if answer.lower() != "y":
        break
    rolls += 1
    print("You got:", roll_dice())
print("You rolled the dice", rolls, "times. Goodbye!")
