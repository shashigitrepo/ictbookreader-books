#: id: ip12-05
#: group: series
#: title: Display the attributes of a Series (index, values, size, dtype, empty) and filter it with Boolean conditions.
#: title_hi: सीरीज़ के गुण (index, values, size, dtype, empty) दिखाइए और बूलियन शर्तों से उसे फ़िल्टर कीजिए।
# Program 5: Series attributes and Boolean indexing
import pandas as pd

price = pd.Series([45.0, 30.5, 120.0, 15.0, 60.0],
                  index=["Pen", "Pencil", "Geometry box", "Eraser", "Notebook"])
print("index :", list(price.index))
print("values:", price.values)
print("size  :", price.size)
print("dtype :", price.dtype)
print("empty :", price.empty)
print("\nItems costing more than 40:")
print(price[price > 40])
print("\nItems between 20 and 60:")
print(price[(price >= 20) & (price <= 60)])
print("\nSorted by price:")
print(price.sort_values())
