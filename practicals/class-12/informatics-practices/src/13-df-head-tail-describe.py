#: id: ip12-13
#: group: dataframe
#: title: Use head(), tail(), sort_values() and aggregate functions (max, min, mean, sum, count) on a DataFrame of student marks.
#: title_hi: विद्यार्थियों के अंकों के डेटाफ़्रेम पर head(), tail(), sort_values() और समूह फ़ंक्शन (max, min, mean, sum, count) का उपयोग कीजिए।
# Program 13: head, tail, sorting and aggregate functions
import pandas as pd

marks = pd.DataFrame({
    "Name": ["Aditya", "Bhumi", "Chaitanya", "Devika", "Farhan", "Gauri"],
    "Maths": [78, 92, 65, 88, 71, 95],
    "IP": [85, 90, 70, 94, 80, 89],
})
print("First 3 rows:")
print(marks.head(3))
print("\nLast 2 rows:")
print(marks.tail(2))
print("\nSorted by IP marks (highest first):")
print(marks.sort_values("IP", ascending=False))
print("\nHighest marks:\n", marks[["Maths", "IP"]].max(), sep="")
print("\nLowest marks:\n", marks[["Maths", "IP"]].min(), sep="")
print("\nAverage marks:\n", marks[["Maths", "IP"]].mean(), sep="")
print("\nTotal of each student:")
marks["Total"] = marks["Maths"] + marks["IP"]
print(marks)
print("\nNumber of students:", marks["Name"].count())
