#: id: cs12-20
#: group: stack
#: title: Write functions PUSH_EVEN(numbers) to push all even numbers of a list onto a stack, and POP_ALL() to pop and display them until the stack is empty.
#: title_hi: फ़ंक्शन PUSH_EVEN(numbers) लिखिए जो सूची की सभी सम संख्याएँ स्टैक में डाले, और POP_ALL() जो स्टैक खाली होने तक उन्हें निकालकर दिखाए।
# Program 20: Push even numbers onto a stack, then pop them all

stack = []


def PUSH_EVEN(numbers):
    for n in numbers:
        if n % 2 == 0:
            stack.append(n)


def POP_ALL():
    while stack:
        print(stack.pop(), end=" ")
    print("\nStack Empty")


nums = [12, 7, 34, 9, 18, 5, 40]
print("List:", nums)
PUSH_EVEN(nums)
print("Stack after pushing even numbers:", stack)
print("Popped elements:")
POP_ALL()
