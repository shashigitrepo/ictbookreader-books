--: id: ip12-25
--: group: sql
--: title: SQL Set 4 – Date functions NOW(), DATE(), MONTH(), MONTHNAME(), YEAR(), DAY() and DAYNAME() on a table of school events.
--: title_hi: SQL सेट 4 – विद्यालय के कार्यक्रमों की तालिका पर दिनांक फ़ंक्शन NOW(), DATE(), MONTH(), MONTHNAME(), YEAR(), DAY() और DAYNAME()।
--: reset: school
--: note: NOW() shows the date and time when the query was run, so its value will be different on your computer.
CREATE DATABASE school;
USE school;
CREATE TABLE events (
  event VARCHAR(20),
  event_date DATE
);
INSERT INTO events VALUES ('Sports Day', '2026-12-05'), ('Science Fair', '2026-08-21'), ('Annual Day', '2027-01-30'), ('Yoga Day', '2026-06-21');
-- Q1. Current date and time, and only today's date.
SELECT NOW(), DATE(NOW());
-- Q2. Day, month number and year of each event.
SELECT event, DAY(event_date), MONTH(event_date), YEAR(event_date) FROM events;
-- Q3. Month name and day name of each event.
SELECT event, MONTHNAME(event_date), DAYNAME(event_date) FROM events;
-- Q4. Events held in the year 2026.
SELECT event FROM events WHERE YEAR(event_date) = 2026;
-- Q5. Events in order of their dates.
SELECT * FROM events ORDER BY event_date;
