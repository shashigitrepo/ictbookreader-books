#: id: ip12-08
#: group: dataframe
#: title: Create a DataFrame for examination results and display its row labels, column labels, data types of each column and its dimensions.
#: title_hi: परीक्षा परिणाम का डेटाफ़्रेम बनाइए और उसके पंक्ति लेबल, स्तंभ लेबल, हर स्तंभ का डेटा टाइप और आयाम (dimensions) दिखाइए।
#: syllabus: yes
# Program 8: Row labels, column labels, dtypes and dimensions
import pandas as pd

result = pd.DataFrame({
    "Name": ["Arnav", "Bela", "Charu", "Dhruv"],
    "Maths": [88, 76, 93, 65],
    "Science": [91, 84, 89, 72],
    "Percent": [89.5, 80.0, 91.0, 68.5],
    "Pass": [True, True, True, True],
}, index=["R1", "R2", "R3", "R4"])
print(result)
print("\nRow labels   :", list(result.index))
print("Column labels:", list(result.columns))
print("\nData types:")
print(result.dtypes)
print("\nShape (rows, columns):", result.shape)
print("Number of dimensions:", result.ndim)
print("Total values (size) :", result.size)
