#: id: cs12-21
#: group: stack
#: title: A dictionary has names of students and their marks. Push the names of students who scored more than 75 onto a stack, then pop and display them.
#: title_hi: एक डिक्शनरी में विद्यार्थियों के नाम और अंक हैं। 75 से अधिक अंक वाले विद्यार्थियों के नाम स्टैक में डालिए, फिर उन्हें निकालकर दिखाइए।
# Program 21: Stack from a dictionary

scores = {"Aditi": 82, "Bhavya": 68, "Chirag": 91, "Divya": 74, "Eshan": 77}
stack = []

for name in scores:
    if scores[name] > 75:
        stack.append(name)
print("Stack:", stack)

print("Popping:")
while stack != []:
    print(stack.pop())
print("Stack is now empty")
