--: id: cs12-28
--: group: sql
--: title: SQL Set 6 – Two tables BOOKS and ISSUED: insert data, display joined details, and update and delete records.
--: title_hi: SQL सेट 6 – दो तालिकाएँ BOOKS और ISSUED: डेटा डालिए, जुड़ा हुआ विवरण दिखाइए तथा रिकॉर्ड अपडेट व डिलीट कीजिए।
--: reset: lib
CREATE DATABASE lib;
USE lib;
CREATE TABLE books (
  bookid CHAR(4) PRIMARY KEY,
  title VARCHAR(25),
  author VARCHAR(20),
  price INT,
  copies INT
);
CREATE TABLE issued (
  bookid CHAR(4),
  student VARCHAR(15),
  issue_date DATE
);
INSERT INTO books VALUES
  ('B001', 'Wings of Fire', 'A P J Abdul Kalam', 350, 5),
  ('B002', 'Godan', 'Premchand', 220, 3),
  ('B003', 'Python Programming', 'R Sharma', 499, 4),
  ('B004', 'The Discovery of India', 'Jawaharlal Nehru', 400, 2);
INSERT INTO issued VALUES
  ('B001', 'Tanvi', '2026-07-10'),
  ('B003', 'Harsh', '2026-07-12'),
  ('B003', 'Ira', '2026-07-15');
-- Title of each issued book with the student's name.
SELECT title, student, issue_date FROM books, issued WHERE books.bookid = issued.bookid;
-- Number of times each book has been issued.
SELECT title, COUNT(*) FROM books, issued WHERE books.bookid = issued.bookid GROUP BY title;
-- Increase the price of books by Premchand by 10%.
UPDATE books SET price = price * 1.1 WHERE author = 'Premchand';
SELECT title, price FROM books;
-- Books costing more than 300, costliest first.
SELECT title, price FROM books WHERE price > 300 ORDER BY price DESC;
-- Remove the issue record of Ira.
DELETE FROM issued WHERE student = 'Ira';
SELECT * FROM issued;
