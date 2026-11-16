#: id: cs12-22
#: group: stack
#: title: Write a program to reverse a string using a stack, and use it to check whether the string is a palindrome.
#: title_hi: स्टैक का उपयोग करके एक स्ट्रिंग उलटने का प्रोग्राम लिखिए और जाँचिए कि स्ट्रिंग पैलिंड्रोम है या नहीं।
#: inputs: madam | stack
# Program 22: Reverse a string using a stack

def reverse(text):
    stack = []
    for ch in text:          # push every character
        stack.append(ch)
    result = ""
    while stack:             # pop them back in reverse order
        result += stack.pop()
    return result


for i in range(2):
    word = input("Enter a word: ")
    rev = reverse(word)
    print("Reversed:", rev)
    print(word, "is a palindrome" if rev == word else "is not a palindrome")
