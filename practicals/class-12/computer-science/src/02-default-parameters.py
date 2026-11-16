#: id: cs12-02
#: group: functions
#: title: Write a function simple_interest(p, r=8, t=2) that uses default parameters, and call it with positional, keyword and default arguments.
#: title_hi: डिफ़ॉल्ट पैरामीटर वाला फ़ंक्शन simple_interest(p, r=8, t=2) लिखिए और इसे पोज़ीशनल, कीवर्ड तथा डिफ़ॉल्ट आर्ग्युमेंट के साथ कॉल कीजिए।
# Program 2: Default, positional and keyword arguments

def simple_interest(p, r=8, t=2):
    """Simple interest = p * r * t / 100 (rate r % per year, time t years)."""
    return p * r * t / 100


print("Only principal (r = 8, t = 2 by default):", simple_interest(10000))
print("Principal and rate (t = 2 by default):  ", simple_interest(10000, 10))
print("All three positional arguments:          ", simple_interest(10000, 10, 3))
print("Keyword arguments in any order:          ", simple_interest(t=5, p=20000, r=6))
