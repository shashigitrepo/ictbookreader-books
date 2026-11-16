--: id: ip12-26
--: group: sql
--: title: SQL Set 5 – Two tables ITEM and SALE: GROUP BY with HAVING, ORDER BY, and an equi-join to show each sale with the item name and amount.
--: title_hi: SQL सेट 5 – दो तालिकाएँ ITEM और SALE: HAVING के साथ GROUP BY, ORDER BY, और हर बिक्री को वस्तु के नाम व राशि के साथ दिखाने के लिए इक्वी-जॉइन।
--: reset: store
CREATE DATABASE store;
USE store;
CREATE TABLE item (
  icode CHAR(3) PRIMARY KEY,
  iname VARCHAR(15),
  price INT
);
CREATE TABLE sale (
  sale_id INT PRIMARY KEY,
  icode CHAR(3),
  qty INT,
  city VARCHAR(10)
);
INSERT INTO item VALUES ('I01', 'Keyboard', 650), ('I02', 'Mouse', 350), ('I03', 'Monitor', 7800), ('I04', 'Webcam', 1900);
INSERT INTO sale VALUES (1, 'I01', 3, 'Delhi'), (2, 'I02', 10, 'Pune'), (3, 'I03', 2, 'Delhi'), (4, 'I02', 6, 'Delhi'), (5, 'I04', 1, 'Pune'), (6, 'I01', 4, 'Pune');
-- Q1. Each sale with the item name and amount (equi-join).
SELECT sale_id, iname, qty, price, qty * price AS amount FROM item, sale WHERE item.icode = sale.icode;
-- Q2. Total quantity sold in each city.
SELECT city, SUM(qty) FROM sale GROUP BY city;
-- Q3. Items sold more than 5 pieces in all.
SELECT iname, SUM(qty) FROM item, sale WHERE item.icode = sale.icode GROUP BY iname HAVING SUM(qty) > 5;
-- Q4. Total sale amount of each item, highest first.
SELECT iname, SUM(qty * price) AS total FROM item, sale WHERE item.icode = sale.icode GROUP BY iname ORDER BY total DESC;
-- Q5. Number of sales and average quantity per city.
SELECT city, COUNT(*), AVG(qty) FROM sale GROUP BY city;
