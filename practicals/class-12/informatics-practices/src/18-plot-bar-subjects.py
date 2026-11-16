#: id: ip12-18
#: group: plots
#: title: Given the school result data, analyse the performance of the students subject-wise and draw a bar graph of the average marks in each subject.
#: title_hi: विद्यालय परिणाम के डेटा से विद्यार्थियों के प्रदर्शन का विषयवार विश्लेषण कीजिए और हर विषय के औसत अंकों का बार ग्राफ़ बनाइए।
#: syllabus: yes
# Program 18: Subject-wise performance (bar graph)
import pandas as pd
import matplotlib.pyplot as plt

result = pd.DataFrame({
    "English": [78, 85, 69, 90, 74],
    "Maths": [92, 66, 81, 88, 59],
    "Physics": [70, 75, 68, 84, 62],
    "Chemistry": [81, 79, 72, 91, 65],
    "IP": [95, 88, 90, 97, 80],
})
average = result.mean()
print("Average marks in each subject:")
print(average)
print("Best subject:", average.idxmax())

plt.bar(average.index, average.values, color=["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f"])
plt.title("Subject-wise Average Marks")
plt.xlabel("Subject")
plt.ylabel("Average marks")
plt.ylim(0, 100)
plt.show()
