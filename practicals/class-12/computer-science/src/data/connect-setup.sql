DROP DATABASE IF EXISTS school;
CREATE DATABASE school;
USE school;
CREATE TABLE student (
  rollno INT PRIMARY KEY,
  name VARCHAR(20),
  stream VARCHAR(12),
  marks INT
);
INSERT INTO student VALUES
  (1, 'Aarav', 'Science', 86),
  (2, 'Diya', 'Commerce', 74),
  (3, 'Kabir', 'Science', 92),
  (4, 'Meera', 'Humanities', 68);
