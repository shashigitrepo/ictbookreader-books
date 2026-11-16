--: id: ip12-23
--: group: sql
--: title: SQL Set 2 – Find the total number of customers from each country in the table CUSTOMER (customer ID, customer name, country) using GROUP BY, with HAVING and ORDER BY.
--: title_hi: SQL सेट 2 – GROUP BY से CUSTOMER तालिका (customer ID, customer name, country) में हर देश के ग्राहकों की कुल संख्या निकालिए; HAVING और ORDER BY के साथ।
--: syllabus: yes
--: reset: shop
CREATE DATABASE shop;
USE shop;
CREATE TABLE customer (
  cust_id INT PRIMARY KEY,
  cust_name VARCHAR(20),
  country VARCHAR(15)
);
INSERT INTO customer VALUES
  (1, 'Arjun Mehta', 'India'), (2, 'Emma Brown', 'UK'), (3, 'Li Wei', 'China'),
  (4, 'Sneha Iyer', 'India'), (5, 'Oliver Smith', 'UK'), (6, 'Rahul Verma', 'India'),
  (7, 'Chen Jing', 'China'), (8, 'Sofia Rossi', 'Italy');
-- Q1. Total number of customers from each country.
SELECT country, COUNT(*) FROM customer GROUP BY country;
-- Q2. Countries with more than one customer.
SELECT country, COUNT(*) AS customers FROM customer GROUP BY country HAVING COUNT(*) > 1;
-- Q3. Countries in descending order of the number of customers.
SELECT country, COUNT(*) AS customers FROM customer GROUP BY country ORDER BY customers DESC;
