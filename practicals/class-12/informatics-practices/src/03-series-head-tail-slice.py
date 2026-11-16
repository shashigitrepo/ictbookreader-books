#: id: ip12-03
#: group: series
#: title: Use head(), tail(), indexing, slicing, loc and iloc on a Series of monthly rainfall.
#: title_hi: मासिक वर्षा की सीरीज़ पर head(), tail(), इंडेक्सिंग, स्लाइसिंग, loc और iloc का उपयोग कीजिए।
# Program 3: head(), tail(), selection, indexing and slicing
import pandas as pd

rain = pd.Series([12, 8, 15, 30, 85, 160, 240, 210, 140, 60, 20, 10],
                 index=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
print("First 3 months (head):")
print(rain.head(3))
print("\nLast 2 months (tail):")
print(rain.tail(2))
print("\nRainfall in July (by label):", rain["Jul"])
print("Rainfall in the 3rd month (by position):", rain.iloc[2])
print("\nJune to September (label slice, end included):")
print(rain.loc["Jun":"Sep"])
print("\nPositions 0 to 2 (position slice, end excluded):")
print(rain.iloc[0:3])
print("\nEvery third month:")
print(rain[::3])
