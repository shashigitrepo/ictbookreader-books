#: id: ip12-14
#: group: csv
#: title: Import data from a CSV file into a DataFrame, process it, and export the result to another CSV file.
#: title_hi: CSV फ़ाइल से डेटा डेटाफ़्रेम में आयात कीजिए, उसे संसाधित कीजिए और परिणाम दूसरी CSV फ़ाइल में निर्यात कीजिए।
#: syllabus: yes
#: files: students.csv
# Program 14: Importing and exporting data between Pandas and CSV files
import pandas as pd

df = pd.read_csv("students.csv")
print("Data read from students.csv:")
print(df)

df["Total"] = df["Maths"] + df["Science"] + df["English"]
df["Percent"] = (df["Total"] / 3).round(2)
toppers = df[df["Percent"] >= 80]
print("\nStudents with 80% or more:")
print(toppers[["Name", "Class", "Percent"]])

toppers.to_csv("toppers.csv", index=False)
print("\nSaved to toppers.csv. Reading it back:")
print(pd.read_csv("toppers.csv"))
