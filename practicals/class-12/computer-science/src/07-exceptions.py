#: id: cs12-07
#: group: exceptions
#: title: Write a program to divide two numbers entered by the user, handling ValueError and ZeroDivisionError with try-except-finally.
#: title_hi: उपयोगकर्ता द्वारा दी गई दो संख्याओं को भाग देने का प्रोग्राम लिखिए जिसमें try-except-finally से ValueError और ZeroDivisionError संभाले जाएँ।
#: inputs: 25 | 4 | 10 | 0 | ten | 9 | 3
# Program 7: Exception handling with try-except-finally

for attempt in range(1, 5):
    print("\nAttempt", attempt)
    try:
        a = int(input("Enter the first number : "))
        b = int(input("Enter the second number: "))
        print("Result =", a / b)
    except ZeroDivisionError:
        print("Error: a number cannot be divided by zero.")
    except ValueError:
        print("Error: please enter whole numbers only.")
    finally:
        print("This line (finally block) always runs.")
