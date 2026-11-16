#: id: ip12-06
#: group: dataframe
#: title: Create a DataFrame from a dictionary of Series and from a list of dictionaries, and display it.
#: title_hi: Series की डिक्शनरी से और डिक्शनरियों की सूची से डेटाफ़्रेम बनाइए और दिखाइए।
# Program 6: DataFrame from a dictionary of Series and a list of dictionaries
import pandas as pd

names = pd.Series(["Ira", "Om", "Pia", "Raj"])
ages = pd.Series([16, 17, 16, 17])
house = pd.Series(["Red", "Blue", "Green", "Blue"])
df1 = pd.DataFrame({"Name": names, "Age": ages, "House": house})
print("From a dictionary of Series:")
print(df1)

rows = [{"City": "Delhi", "Temp": 31, "Humidity": 45},
        {"City": "Chennai", "Temp": 34, "Humidity": 70},
        {"City": "Shimla", "Temp": 18}]          # Humidity missing for Shimla
df2 = pd.DataFrame(rows)
print("\nFrom a list of dictionaries (missing value becomes NaN):")
print(df2)
