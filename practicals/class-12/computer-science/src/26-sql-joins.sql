--: id: cs12-26
--: group: sql
--: title: SQL Set 4 – Two tables DEPT and EMP: Cartesian product, equi-join and natural join.
--: title_hi: SQL सेट 4 – दो तालिकाएँ DEPT और EMP: कार्टेशियन गुणनफल (Cartesian product), इक्वी-जॉइन और नेचुरल जॉइन।
--: syllabus: yes
--: reset: office
CREATE DATABASE office;
USE office;
CREATE TABLE dept (
  deptno INT PRIMARY KEY,
  dname VARCHAR(15),
  location VARCHAR(15)
);
CREATE TABLE emp (
  empno INT PRIMARY KEY,
  ename VARCHAR(15),
  salary INT,
  deptno INT,
  FOREIGN KEY (deptno) REFERENCES dept(deptno)
);
INSERT INTO dept VALUES (10, 'Accounts', 'Delhi'), (20, 'Research', 'Mumbai'), (30, 'Sales', 'Chennai');
INSERT INTO emp VALUES (1, 'Asha', 45000, 10), (2, 'Vikram', 62000, 20), (3, 'Neel', 38000, 30), (4, 'Ruchi', 51000, 20);
-- Cartesian product of the two tables (every row with every row).
SELECT ename, dname FROM emp, dept;
-- Equi-join: each employee with the name and location of the department.
SELECT e.ename, e.salary, d.dname, d.location
FROM emp e, dept d
WHERE e.deptno = d.deptno;
-- Natural join (joins on the common column DEPTNO automatically).
SELECT * FROM emp NATURAL JOIN dept;
-- Employees working in Mumbai.
SELECT ename FROM emp, dept WHERE emp.deptno = dept.deptno AND location = 'Mumbai';
-- Number of employees and total salary in each department.
SELECT dname, COUNT(*), SUM(salary)
FROM emp, dept
WHERE emp.deptno = dept.deptno
GROUP BY dname;
