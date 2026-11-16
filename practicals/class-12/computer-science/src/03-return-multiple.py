#: id: cs12-03
#: group: functions
#: title: Write a function stats(numbers) that returns the largest, smallest and average of a list of numbers (a function returning more than one value).
#: title_hi: एक फ़ंक्शन stats(numbers) लिखिए जो सूची की सबसे बड़ी, सबसे छोटी संख्या और औसत लौटाए (एक से अधिक मान लौटाने वाला फ़ंक्शन)।
#: inputs: 45 78 12 90 33 61
# Program 3: Function returning multiple values

def stats(numbers):
    largest = max(numbers)
    smallest = min(numbers)
    average = sum(numbers) / len(numbers)
    return largest, smallest, average      # returned together as a tuple


values = [int(x) for x in input("Enter numbers separated by spaces: ").split()]
big, small, avg = stats(values)
print("Largest :", big)
print("Smallest:", small)
print("Average :", round(avg, 2))
print("Returned as a tuple:", stats(values))
