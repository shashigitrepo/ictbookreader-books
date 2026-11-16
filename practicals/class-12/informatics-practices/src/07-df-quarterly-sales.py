#: id: ip12-07
#: group: dataframe
#: title: Create a DataFrame quarterly sales where each row contains the item category, item name and expenditure. Group the rows by category and print the total expenditure per category.
#: title_hi: तिमाही बिक्री का डेटाफ़्रेम बनाइए जिसकी हर पंक्ति में वस्तु श्रेणी, वस्तु का नाम और व्यय हो। पंक्तियों को श्रेणी के अनुसार समूहित करके प्रति श्रेणी कुल व्यय प्रिंट कीजिए।
#: syllabus: yes
# Program 7: Group by category and total expenditure
import pandas as pd

sales = pd.DataFrame({
    "Category": ["Electronics", "Furniture", "Electronics", "Stationery",
                 "Furniture", "Stationery", "Electronics"],
    "Item": ["Laptop", "Chair", "Printer", "Notebooks", "Table", "Pens", "Mouse"],
    "Expenditure": [55000, 4500, 12000, 1800, 9000, 600, 900],
})
print(sales)
print("\nTotal expenditure per category:")
print(sales.groupby("Category")["Expenditure"].sum())
