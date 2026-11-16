#: id: ip12-10
#: group: dataframe
#: title: Iterate over the rows of a DataFrame using iterrows() and over its columns using items().
#: title_hi: iterrows() से डेटाफ़्रेम की पंक्तियों पर और items() से उसके स्तंभों पर पुनरावृत्ति (iteration) कीजिए।
# Program 10: Iterating over a DataFrame
import pandas as pd

df = pd.DataFrame({"Item": ["Rice", "Dal", "Oil"],
                   "Qty": [5, 2, 1],
                   "Rate": [60, 120, 180]})

print("Row by row (iterrows):")
for idx, row in df.iterrows():
    print(idx, row["Item"], "costs", row["Qty"] * row["Rate"])

print("\nColumn by column (items):")
for col, values in df.items():
    print(col, ":", list(values))
