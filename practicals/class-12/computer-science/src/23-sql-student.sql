--: id: cs12-23
--: group: sql
--: title: SQL Set 1 – Create a STUDENT table, insert data and use ALTER (add / modify / drop attribute), UPDATE, ORDER BY, DELETE, and GROUP BY with MIN, MAX, SUM, COUNT and AVG.
--: title_hi: SQL सेट 1 – STUDENT तालिका बनाइए, डेटा डालिए और ALTER (कॉलम जोड़ना / बदलना / हटाना), UPDATE, ORDER BY, DELETE तथा MIN, MAX, SUM, COUNT, AVG के साथ GROUP BY का उपयोग कीजिए।
--: syllabus: yes
--: reset: school
-- Create a database SCHOOL and open it.
CREATE DATABASE school;
USE school;
-- Create the table STUDENT.
CREATE TABLE student (
  rollno INT PRIMARY KEY,
  name VARCHAR(20) NOT NULL,
  class CHAR(3),
  stream VARCHAR(12),
  marks INT
);
-- Insert six records.
INSERT INTO student VALUES
  (1, 'Aarav', 'XII', 'Science', 86),
  (2, 'Diya', 'XII', 'Commerce', 74),
  (3, 'Kabir', 'XII', 'Science', 92),
  (4, 'Meera', 'XII', 'Humanities', 68),
  (5, 'Rohan', 'XII', 'Commerce', 81),
  (6, 'Sara', 'XII', 'Science', 77);
SELECT * FROM student;
-- Add a new attribute CITY.
ALTER TABLE student ADD city VARCHAR(15);
-- Change the data type of NAME to VARCHAR(30).
ALTER TABLE student MODIFY name VARCHAR(30);
DESCRIBE student;
-- Remove the attribute CITY.
ALTER TABLE student DROP city;
-- Give 5 grace marks to students of the Humanities stream.
UPDATE student SET marks = marks + 5 WHERE stream = 'Humanities';
-- Display the names and marks in descending order of marks.
SELECT name, marks FROM student ORDER BY marks DESC;
-- Delete the record of roll number 6.
DELETE FROM student WHERE rollno = 6;
-- Stream-wise lowest, highest, total, number and average marks.
SELECT stream, MIN(marks), MAX(marks), SUM(marks), COUNT(*), AVG(marks)
FROM student GROUP BY stream;
