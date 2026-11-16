#: id: ip12-04
#: group: series
#: title: Given a Series, print all the elements that are above the 75th percentile.
#: title_hi: दी गई सीरीज़ के वे सभी तत्व प्रिंट कीजिए जो 75वें प्रतिशतक (percentile) से ऊपर हैं।
#: syllabus: yes
# Program 4: Elements above the 75th percentile
import pandas as pd

scores = pd.Series([56, 78, 91, 45, 83, 67, 99, 72, 88, 61],
                   index=["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10"])
p75 = scores.quantile(0.75)
print("75th percentile =", p75)
print("Scores above the 75th percentile:")
print(scores[scores > p75])
