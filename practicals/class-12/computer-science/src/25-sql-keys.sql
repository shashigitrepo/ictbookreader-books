--: id: cs12-25
--: group: sql
--: title: SQL Set 3 – Database and table commands: SHOW DATABASES, USE, SHOW TABLES, DESCRIBE, adding and removing a PRIMARY KEY, constraints NOT NULL and UNIQUE, and DROP TABLE.
--: title_hi: SQL सेट 3 – डेटाबेस और तालिका कमांड: SHOW DATABASES, USE, SHOW TABLES, DESCRIBE, PRIMARY KEY जोड़ना व हटाना, NOT NULL व UNIQUE बाधाएँ (constraints) और DROP TABLE।
--: reset: school, company, library, office, shop, lib
CREATE DATABASE library;
SHOW DATABASES;
USE library;
-- Create a table without a primary key.
CREATE TABLE member (
  memid INT NOT NULL,
  name VARCHAR(25) NOT NULL,
  phone CHAR(10) UNIQUE,
  city VARCHAR(15)
);
SHOW TABLES;
DESCRIBE member;
-- Make MEMID the primary key.
ALTER TABLE member ADD PRIMARY KEY (memid);
DESCRIBE member;
INSERT INTO member VALUES (1, 'Priya', '9876500001', 'Delhi');
-- Inserting the same MEMID again breaks the primary key.
INSERT INTO member VALUES (1, 'Rahul', '9876500002', 'Pune');
-- Inserting a NULL name breaks the NOT NULL constraint.
INSERT INTO member VALUES (2, NULL, '9876500003', 'Agra');
-- Remove the primary key.
ALTER TABLE member DROP PRIMARY KEY;
DESCRIBE member;
-- Delete the table.
DROP TABLE member;
SHOW TABLES;
