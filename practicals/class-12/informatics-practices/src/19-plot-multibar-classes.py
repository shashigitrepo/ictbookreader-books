#: id: ip12-19
#: group: plots
#: title: For class-wise result data in a DataFrame, compare the pass percentage of sections in two years with a multiple bar chart that has a title and a legend.
#: title_hi: डेटाफ़्रेम में कक्षावार परिणाम डेटा के लिए, दो वर्षों में अनुभागों (sections) के उत्तीर्ण प्रतिशत की तुलना शीर्षक और लेजेंड वाले बहु-बार चार्ट से कीजिए।
#: syllabus: yes
# Program 19: Class-wise comparison (multiple bar chart with legend)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({"Section": ["XII-A", "XII-B", "XII-C", "XII-D"],
                   "2025": [92, 85, 78, 88],
                   "2026": [95, 89, 84, 86]})
print(df)
x = np.arange(len(df))
width = 0.35
plt.bar(x - width / 2, df["2025"], width, label="2025")
plt.bar(x + width / 2, df["2026"], width, label="2026")
plt.xticks(x, df["Section"])
plt.title("Pass Percentage by Section")
plt.xlabel("Section")
plt.ylabel("Pass percentage")
plt.ylim(0, 110)
plt.legend()
plt.show()
