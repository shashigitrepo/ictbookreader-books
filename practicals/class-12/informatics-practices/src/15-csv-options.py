#: id: ip12-15
#: group: csv
#: title: Read a CSV file with options (usecols, index_col, nrows) and write a DataFrame to CSV with a different separator and without the index.
#: title_hi: विकल्पों (usecols, index_col, nrows) के साथ CSV फ़ाइल पढ़िए और डेटाफ़्रेम को अलग विभाजक (separator) के साथ, बिना इंडेक्स के CSV में लिखिए।
#: files: students.csv
# Program 15: read_csv() and to_csv() options
import pandas as pd

part = pd.read_csv("students.csv", usecols=["Name", "Maths"], nrows=3)
print("Only two columns, first 3 rows:")
print(part)

by_roll = pd.read_csv("students.csv", index_col="RollNo")
print("\nRollNo used as the row index:")
print(by_roll.head())

class_a = by_roll[by_roll["Class"] == "XII-A"]
class_a.to_csv("class_a.csv", sep=";", index=False)
print("\nContents of class_a.csv (separator ;):")
with open("class_a.csv") as f:
    print(f.read(), end="")
