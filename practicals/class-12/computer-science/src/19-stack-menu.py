#: id: cs12-19
#: group: stack
#: title: Write a Python program to implement a stack using a list (menu-driven: push, pop, peek, display).
#: title_hi: सूची (list) का उपयोग करके स्टैक लागू करने का पायथन प्रोग्राम लिखिए (मेनू-आधारित: push, pop, peek, display)।
#: syllabus: yes
#: inputs: 1 | 10 | 1 | 20 | 1 | 30 | 4 | 3 | 2 | 4 | 2 | 2 | 2 | 5
# Program 19: Stack using a list

stack = []


def push(item):
    stack.append(item)


def pop():
    if stack == []:
        return "Underflow"           # nothing to remove
    return stack.pop()


def peek():
    if stack == []:
        return "Underflow"
    return stack[-1]


def display():
    if stack == []:
        print("Stack is empty")
    else:
        print("Stack (top first):", *stack[::-1])


while True:
    print("\n1.Push  2.Pop  3.Peek  4.Display  5.Exit")
    ch = int(input("Enter choice: "))
    if ch == 1:
        push(int(input("Enter element: ")))
    elif ch == 2:
        print("Popped:", pop())
    elif ch == 3:
        print("Top element:", peek())
    elif ch == 4:
        display()
    elif ch == 5:
        break
    else:
        print("Invalid choice")
