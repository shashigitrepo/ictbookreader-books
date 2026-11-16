#: id: ip12-21
#: group: plots
#: title: Plot the monthly sales of two shops from a DataFrame as a line chart with two lines, different styles, a legend and a title.
#: title_hi: डेटाफ़्रेम से दो दुकानों की मासिक बिक्री को दो रेखाओं, अलग शैलियों, लेजेंड और शीर्षक वाले लाइन चार्ट में दिखाइए।
# Program 21: Line chart with two lines and a legend
import pandas as pd
import matplotlib.pyplot as plt

sales = pd.DataFrame({"Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                      "Shop A": [42, 48, 51, 47, 60, 66],
                      "Shop B": [38, 41, 49, 55, 58, 52]})
print(sales)
plt.plot(sales["Month"], sales["Shop A"], color="blue", marker="s", label="Shop A")
plt.plot(sales["Month"], sales["Shop B"], color="red", marker="^", linestyle="--", label="Shop B")
plt.title("Monthly Sales (in thousand rupees)")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.legend()
plt.show()
