#: id: cs12-05
#: group: functions
#: title: Write functions is_palindrome(n) and is_armstrong(n), and use them to check numbers entered by the user.
#: title_hi: फ़ंक्शन is_palindrome(n) और is_armstrong(n) लिखिए तथा उपयोगकर्ता द्वारा दी गई संख्याओं की जाँच कीजिए।
#: inputs: 121 | 153 | 370 | 123
# Program 5: Palindrome and Armstrong numbers

def is_palindrome(n):
    return str(n) == str(n)[::-1]


def is_armstrong(n):
    digits = str(n)
    power = len(digits)
    total = 0
    for d in digits:
        total += int(d) ** power
    return total == n


for i in range(4):
    num = int(input("Enter a number: "))
    print(num, "is a palindrome" if is_palindrome(num) else "is not a palindrome", end="; ")
    print("an Armstrong number" if is_armstrong(num) else "not an Armstrong number")
