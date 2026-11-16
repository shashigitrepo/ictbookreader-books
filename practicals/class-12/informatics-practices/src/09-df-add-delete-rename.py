#: id: ip12-09
#: group: dataframe
#: title: Add, select, delete and rename rows and columns of a DataFrame.
#: title_hi: डेटाफ़्रेम की पंक्तियाँ और स्तंभ जोड़िए, चुनिए, हटाइए और उनका नाम बदलिए।
# Program 9: Operations on rows and columns
import pandas as pd

df = pd.DataFrame({"Hindi": [78, 85, 69], "English": [82, 74, 90]},
                  index=["Anu", "Bilal", "Charvi"])
print("Original:")
print(df)

df["Maths"] = [91, 66, 88]                 # add a column
df.loc["Deep"] = [72, 80, 77]              # add a row
print("\nAfter adding column Maths and row Deep:")
print(df)

print("\nSelect column English:")
print(df["English"])
print("\nSelect row Bilal:")
print(df.loc["Bilal"])

df = df.drop("Hindi", axis=1)              # delete a column
df = df.drop("Charvi")                     # delete a row
df = df.rename(columns={"English": "Eng"}, index={"Anu": "Anushka"})
print("\nAfter deleting Hindi and Charvi, and renaming:")
print(df)
