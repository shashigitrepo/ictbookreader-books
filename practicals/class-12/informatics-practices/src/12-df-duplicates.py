#: id: ip12-12
#: group: dataframe
#: title: Filter out rows based on different criteria, such as duplicate rows.
#: title_hi: विभिन्न मानदंडों के आधार पर पंक्तियाँ छाँटिए, जैसे दोहराई गई (duplicate) पंक्तियाँ।
#: syllabus: yes
# Program 12: Finding and removing duplicate rows
import pandas as pd

entries = pd.DataFrame({
    "RollNo": [1, 2, 2, 3, 4, 4, 5],
    "Name": ["Aman", "Bina", "Bina", "Chirag", "Disha", "Disha", "Ekta"],
    "Event": ["Race", "Quiz", "Quiz", "Chess", "Dance", "Quiz", "Race"],
})
print("All entries:")
print(entries)
print("\nIs the row a duplicate of an earlier row?")
print(entries.duplicated())
print("\nDuplicate rows:")
print(entries[entries.duplicated()])
print("\nAfter removing duplicate rows:")
print(entries.drop_duplicates())
print("\nOne row per student (duplicates by RollNo removed):")
print(entries.drop_duplicates(subset="RollNo"))
print("\nOnly the Quiz entries:")
print(entries[entries["Event"] == "Quiz"])
