--: id: cs12-27
--: group: sql
--: title: SQL Set 5 – On a SALES table, use aggregate functions with GROUP BY and HAVING, and sort the result with ORDER BY.
--: title_hi: SQL सेट 5 – SALES तालिका पर GROUP BY और HAVING के साथ समूह फ़ंक्शन (aggregate functions) और ORDER BY से परिणाम क्रमबद्ध कीजिए।
--: reset: shop
CREATE DATABASE shop;
USE shop;
CREATE TABLE sales (
  billno INT PRIMARY KEY,
  item VARCHAR(15),
  category VARCHAR(12),
  qty INT,
  rate INT
);
INSERT INTO sales VALUES
  (1, 'Notebook', 'Stationery', 20, 40),
  (2, 'Pen', 'Stationery', 50, 10),
  (3, 'Apple', 'Fruits', 12, 120),
  (4, 'Banana', 'Fruits', 24, 50),
  (5, 'Milk', 'Dairy', 30, 60),
  (6, 'Paneer', 'Dairy', 5, 400),
  (7, 'Pencil', 'Stationery', 40, 5);
-- Total quantity sold in each category.
SELECT category, SUM(qty) FROM sales GROUP BY category;
-- Sale amount (qty x rate) of each category, highest first.
SELECT category, SUM(qty * rate) AS amount
FROM sales GROUP BY category ORDER BY amount DESC;
-- Categories having more than two items.
SELECT category, COUNT(*) FROM sales GROUP BY category HAVING COUNT(*) > 2;
-- Categories whose average rate is more than 100.
SELECT category, AVG(rate) FROM sales GROUP BY category HAVING AVG(rate) > 100;
-- Costliest and cheapest rate.
SELECT MAX(rate), MIN(rate) FROM sales;
-- Number of different categories.
SELECT COUNT(DISTINCT category) FROM sales;
