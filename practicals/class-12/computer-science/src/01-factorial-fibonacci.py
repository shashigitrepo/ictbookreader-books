#: id: cs12-01
#: group: functions
#: title: Write a menu-driven program using user-defined functions to find the factorial of a number and to display the first n terms of the Fibonacci series.
#: title_hi: उपयोगकर्ता-परिभाषित फ़ंक्शन का उपयोग करके किसी संख्या का फ़ैक्टोरियल ज्ञात करने और फ़िबोनाची श्रेणी के पहले n पद दिखाने का मेनू-आधारित प्रोग्राम लिखिए।
#: inputs: 1 | 6 | 2 | 10 | 3
# Program 1: Factorial and Fibonacci series using functions

def factorial(n):
    """Returns n! (n factorial)."""
    result = 1
    for i in range(1, n + 1):
        result = result * i
    return result


def fibonacci(n):
    """Returns a list with the first n terms of the Fibonacci series."""
    terms = []
    a, b = 0, 1
    for i in range(n):
        terms.append(a)
        a, b = b, a + b
    return terms


while True:
    print("\n1. Factorial of a number")
    print("2. Fibonacci series")
    print("3. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        num = int(input("Enter a number: "))
        print("Factorial of", num, "is", factorial(num))
    elif choice == 2:
        n = int(input("How many terms? "))
        print("Fibonacci series:", *fibonacci(n))
    elif choice == 3:
        print("Thank you!")
        break
    else:
        print("Invalid choice")
