#: id: cs12-04
#: group: functions
#: title: Write a program to show the difference between global and local scope of variables, and the use of the global keyword.
#: title_hi: चरों के ग्लोबल और लोकल स्कोप का अंतर तथा global कीवर्ड का उपयोग दिखाने का प्रोग्राम लिखिए।
# Program 4: Scope of variables (global and local)

count = 10                  # global variable


def show_local():
    count = 5               # a new local variable with the same name
    print("Inside show_local(), local count =", count)


def change_global():
    global count            # refer to the global variable
    count = count + 1
    print("Inside change_global(), global count =", count)


print("Before calls, count =", count)
show_local()
print("After show_local(), count =", count)
change_global()
print("After change_global(), count =", count)
