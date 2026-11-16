--: id: ip12-22
--: group: sql
--: title: SQL Set 1 – Create a STUDENT table with student id, name and marks (student id as the primary key); insert, delete and select records; find MIN, MAX, SUM and AVG of marks; and order the records by marks.
--: title_hi: SQL सेट 1 – student id, name और marks वाली STUDENT तालिका बनाइए (student id प्राथमिक कुंजी); रिकॉर्ड डालिए, हटाइए और चुनिए; अंकों का MIN, MAX, SUM, AVG निकालिए और रिकॉर्ड अंकों के क्रम में लगाइए।
--: syllabus: yes
--: reset: school
CREATE DATABASE school;
USE school;
-- Q1. Create a student table with the student id, name and marks as attributes where the student id is the primary key.
CREATE TABLE student (
  stud_id INT PRIMARY KEY,
  name VARCHAR(20),
  marks INT
);
INSERT INTO student VALUES (101, 'Ayesha', 78), (102, 'Bharat', 91), (103, 'Charu', 64), (104, 'Dev', 85), (105, 'Ela', 72);
-- Q2. Insert the details of a new student in the above table.
INSERT INTO student VALUES (106, 'Faiz', 88);
SELECT * FROM student;
-- Q3. Delete the details of a student in the above table.
DELETE FROM student WHERE stud_id = 103;
-- Q4. Use the select command to get the details of the students with marks more than 80.
SELECT * FROM student WHERE marks > 80;
-- Q5. Find the min, max, sum, and average of the marks in the student marks table.
SELECT MIN(marks), MAX(marks), SUM(marks), AVG(marks) FROM student;
-- Q6. Order the (student ID, marks) table in descending order of the marks.
SELECT stud_id, marks FROM student ORDER BY marks DESC;
