#: id: ip12-02
#: group: series
#: title: Create a Series from a scalar value, and perform mathematical operations (+, -, *, /) on two Series.
#: title_hi: एक अदिश (scalar) मान से सीरीज़ बनाइए और दो सीरीज़ पर गणितीय संक्रियाएँ (+, -, *, /) कीजिए।
# Program 2: Series from a scalar and mathematical operations
import pandas as pd

fee = pd.Series(1500, index=["Jan", "Feb", "Mar"])
print("Series from a scalar value:")
print(fee)

term1 = pd.Series([45, 38, 50, 41], index=["Asha", "Ben", "Chen", "Dev"])
term2 = pd.Series([48, 42, 47, 44], index=["Asha", "Ben", "Chen", "Dev"])
print("\nTotal (term1 + term2):")
print(term1 + term2)
print("\nImprovement (term2 - term1):")
print(term2 - term1)
print("\nTerm 1 marks doubled (term1 * 2):")
print(term1 * 2)
print("\nPercentage of term 2 out of 50 (term2 / 50 * 100):")
print(term2 / 50 * 100)
