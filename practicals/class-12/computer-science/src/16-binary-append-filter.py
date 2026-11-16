#: id: cs12-16
#: group: binary-files
#: title: Append employee records (code, name, salary) to a binary file and display the employees whose salary is more than 50000.
#: title_hi: बाइनरी फ़ाइल में कर्मचारी रिकॉर्ड (कोड, नाम, वेतन) जोड़िए और 50000 से अधिक वेतन वाले कर्मचारी दिखाइए।
#: inputs: E01 | Neha | 48000 | y | E02 | Arjun | 62000 | y | E03 | Farah | 55000 | n
# Program 16: Append to a binary file and filter records
import pickle

while True:
    code = input("Employee code: ")
    name = input("Name         : ")
    salary = int(input("Salary       : "))
    with open("emp.dat", "ab") as f:          # ab = append in binary mode
        pickle.dump({"code": code, "name": name, "salary": salary}, f)
    if input("Add another? (y/n): ").lower() != "y":
        break

print("\nEmployees earning more than 50000:")
with open("emp.dat", "rb") as f:
    try:
        while True:
            emp = pickle.load(f)
            if emp["salary"] > 50000:
                print(emp["code"], emp["name"], emp["salary"])
    except EOFError:
        pass
