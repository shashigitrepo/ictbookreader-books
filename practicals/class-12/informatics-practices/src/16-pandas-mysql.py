#: id: ip12-16
#: group: csv
#: title: Export a DataFrame to a MySQL table using to_sql(), and import the data back into Pandas using read_sql() with a query.
#: title_hi: to_sql() से डेटाफ़्रेम को MySQL तालिका में निर्यात कीजिए और क्वेरी के साथ read_sql() से डेटा वापस Pandas में आयात कीजिए।
#: setup: ip-sql-setup.sql
#: files: students.csv
# Program 16: Importing and exporting data between Pandas and MySQL
import pandas as pd
from sqlalchemy import create_engine

# mysql+pymysql://user:password@host/database
engine = create_engine("mysql+pymysql://root:tiger@localhost/school")

df = pd.read_csv("students.csv")
df.to_sql("marks", engine, if_exists="replace", index=False)
print("DataFrame saved as table MARKS in MySQL")

result = pd.read_sql("SELECT Name, Class, Maths FROM marks WHERE Maths > 75", engine)
print("\nStudents with more than 75 in Maths (read from MySQL):")
print(result)

avg = pd.read_sql("SELECT Class, AVG(Science) AS AvgScience FROM marks GROUP BY Class", engine)
print("\nClass-wise average in Science:")
print(avg)
