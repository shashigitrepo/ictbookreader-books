--: id: ip12-24
--: group: sql
--: title: SQL Set 3 – Math functions POWER(), ROUND(), MOD() and text functions UPPER(), LOWER(), SUBSTR(), MID(), LENGTH(), LEFT(), RIGHT(), INSTR(), LTRIM(), RTRIM(), TRIM().
--: title_hi: SQL सेट 3 – गणितीय फ़ंक्शन POWER(), ROUND(), MOD() तथा टेक्स्ट फ़ंक्शन UPPER(), LOWER(), SUBSTR(), MID(), LENGTH(), LEFT(), RIGHT(), INSTR(), LTRIM(), RTRIM(), TRIM()।
--: reset: shop
CREATE DATABASE shop;
USE shop;
CREATE TABLE product (
  pcode CHAR(4) PRIMARY KEY,
  pname VARCHAR(20),
  price FLOAT,
  qty INT
);
INSERT INTO product VALUES ('P01', 'Steel Bottle', 349.75, 12), ('P02', 'Lunch Box', 225.40, 7), ('P03', 'School Bag', 899.99, 5), ('P04', 'Water Colour', 120.50, 20);
-- Q1. POWER(): square of the quantity of each product.
SELECT pname, qty, POWER(qty, 2) FROM product;
-- Q2. ROUND(): price rounded to 1 decimal place and to the nearest rupee.
SELECT pname, ROUND(price, 1), ROUND(price) FROM product;
-- Q3. MOD(): remainder when the quantity is divided by 5.
SELECT pname, qty, MOD(qty, 5) FROM product;
-- Q4. UPPER() and LOWER().
SELECT UPPER(pname), LOWER(pname) FROM product;
-- Q5. LENGTH(), LEFT() and RIGHT().
SELECT pname, LENGTH(pname), LEFT(pname, 3), RIGHT(pname, 3) FROM product;
-- Q6. SUBSTR() / MID(): 4 characters from the 2nd character.
SELECT pname, SUBSTR(pname, 2, 4), MID(pname, 2, 4) FROM product;
-- Q7. INSTR(): position of the first 'o' in the product name.
SELECT pname, INSTR(pname, 'o') FROM product;
-- Q8. LTRIM(), RTRIM() and TRIM() on a string with spaces.
SELECT CONCAT('[', LTRIM('   Padhaku   '), ']') AS ltrimmed,
       CONCAT('[', RTRIM('   Padhaku   '), ']') AS rtrimmed,
       CONCAT('[', TRIM('   Padhaku   '), ']') AS trimmed;
