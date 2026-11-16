#: id: ip12-01
#: group: series
#: title: Create a Pandas Series from a dictionary of values and from an ndarray.
#: title_hi: मानों की डिक्शनरी से और ndarray से Pandas सीरीज़ बनाइए।
#: syllabus: yes
# Program 1: Series from a dictionary and from an ndarray
import pandas as pd
import numpy as np

marks = {"English": 82, "Maths": 91, "Physics": 76, "Chemistry": 88, "IP": 95}
s1 = pd.Series(marks)
print("Series from a dictionary:")
print(s1)

arr = np.array([12.5, 15.0, 17.5, 20.0])
s2 = pd.Series(arr, index=["Q1", "Q2", "Q3", "Q4"])
print("\nSeries from an ndarray:")
print(s2)
