#: id: ip12-20
#: group: plots
#: title: Draw a histogram of the marks of 30 students in IP to show how many students fall in each range of marks.
#: title_hi: IP में 30 विद्यार्थियों के अंकों का हिस्टोग्राम बनाइए जो दिखाए कि अंकों की हर सीमा में कितने विद्यार्थी हैं।
# Program 20: Histogram of marks
import matplotlib.pyplot as plt

marks = [45, 52, 58, 61, 63, 66, 68, 70, 71, 72, 74, 75, 76, 78, 79,
         80, 81, 82, 83, 85, 86, 87, 88, 90, 91, 92, 94, 95, 97, 99]
counts, edges, bars = plt.hist(marks, bins=[40, 50, 60, 70, 80, 90, 100],
                               color="orange", edgecolor="black")
for low, high, c in zip(edges[:-1], edges[1:], counts):
    print(f"{int(low)}-{int(high)}: {int(c)} students")
plt.title("Distribution of IP Marks")
plt.xlabel("Marks")
plt.ylabel("Number of students")
plt.show()
