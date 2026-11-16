--: id: cs12-24
--: group: sql
--: title: SQL Set 2 – On an EMPLOYEE table, use relational and logical operators, BETWEEN, IN, LIKE, IS NULL / IS NOT NULL, DISTINCT and column aliases.
--: title_hi: SQL सेट 2 – EMPLOYEE तालिका पर संबंधात्मक व तार्किक ऑपरेटर, BETWEEN, IN, LIKE, IS NULL / IS NOT NULL, DISTINCT और कॉलम उपनाम (alias) का उपयोग कीजिए।
--: reset: company
CREATE DATABASE company;
USE company;
CREATE TABLE employee (
  empid CHAR(4) PRIMARY KEY,
  name VARCHAR(20),
  dept VARCHAR(12),
  salary INT,
  bonus INT,
  doj DATE
);
INSERT INTO employee VALUES
  ('E101', 'Anil Kumar', 'Sales', 42000, 3000, '2019-04-12'),
  ('E102', 'Bindu Rao', 'Accounts', 55000, NULL, '2017-08-01'),
  ('E103', 'Chetan Das', 'IT', 68000, 5000, '2020-01-15'),
  ('E104', 'Deepa Nair', 'Sales', 39000, NULL, '2022-06-20'),
  ('E105', 'Gaurav Jain', 'IT', 72000, 6000, '2016-11-03'),
  ('E106', 'Anita Roy', 'Accounts', 47000, 2500, '2021-09-09');
-- Employees of the IT department earning more than 70000.
SELECT * FROM employee WHERE dept = 'IT' AND salary > 70000;
-- Employees with salary between 40000 and 60000.
SELECT name, salary FROM employee WHERE salary BETWEEN 40000 AND 60000;
-- Employees of the Sales or Accounts department.
SELECT name, dept FROM employee WHERE dept IN ('Sales', 'Accounts');
-- Names starting with 'A'.
SELECT name FROM employee WHERE name LIKE 'A%';
-- Names whose second letter is 'i'.
SELECT name FROM employee WHERE name LIKE '_i%';
-- Employees who did not get a bonus.
SELECT name FROM employee WHERE bonus IS NULL;
-- Employees who got a bonus.
SELECT name, bonus FROM employee WHERE bonus IS NOT NULL;
-- Different departments (without repetition).
SELECT DISTINCT dept FROM employee;
-- Annual salary with a column alias.
SELECT name, salary * 12 AS annual_salary FROM employee;
-- Employees who joined before 2019.
SELECT name, doj FROM employee WHERE doj < '2019-01-01';
