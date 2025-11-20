--
-- Name: Cole Determan
--
-- Write your queries below each comment. Please use good style (one clause
-- per line, JOIN syntax, indentation) and make sure all queries end with a
-- semicolon. When necessary, limit the output to the first 200 results.
--
-- DO NOT MODIFY OR DELETE ANY OTHER LINES!
--

-- -----------------------------------------------------------------------------
-- Connect to air database
\c air
-- -----------------------------------------------------------------------------

--
\echo
\echo Query #1
--
-- List all last names in the database that start with the letter M. Use the
-- lower() function to convert all last names to lowercase. Show how many times
-- each last name is used. Note: last names are in more than one table.
--
-- Schema: count, last_name
--  Order: count (descending), last_name

SELECT
    COUNT(*) AS count,
    LOWER(last_name) AS last_name
FROM (
    SELECT last_name FROM passenger
    UNION ALL
    SELECT last_name FROM account
    UNION ALL
    SELECT last_name FROM frequent_flyer
) AS all_last_names
WHERE LOWER(last_name) LIKE 'm%'
GROUP BY LOWER(last_name)
ORDER BY count DESC, last_name
LIMIT 200;


--
\echo
\echo Query #2
--
-- Show the passengers who have flown out of Dulles (IAD) but have never flown
-- out of Orlando (MCO).
--
-- Schema: passenger_id, first_name, last_name
--  Order: passenger_id

SELECT
    p.passenger_id,
    p.first_name,
    p.last_name
FROM passenger AS p
WHERE EXISTS (
        SELECT 1
        FROM booking AS b
        JOIN booking_leg AS bl
          ON b.booking_id = bl.booking_id
        JOIN flight AS f
          ON bl.flight_id = f.flight_id
        WHERE b.booking_id = p.booking_id
          AND f.departure_airport = 'IAD'
    )
  AND NOT EXISTS (
        SELECT 1
        FROM booking AS b
        JOIN booking_leg AS bl
          ON b.booking_id = bl.booking_id
        JOIN flight AS f
          ON bl.flight_id = f.flight_id
        WHERE b.booking_id = p.booking_id
          AND f.departure_airport = 'MCO'
    )
ORDER BY p.passenger_id
LIMIT 200;


--
\echo
\echo Query #3
--
-- Find the passengers who have not been issued a boarding pass, but whose
-- booked itinerary includes a domestic flight from Dhaka (depart airport
-- DAC, arrive in Bangladesh BD).
--
-- Schema: first_name, last_name, iso_country
--  Order: passenger_id

SELECT
    p.first_name,
    p.last_name,
    a_arr.iso_country
FROM passenger AS p
JOIN booking AS b
  ON p.booking_id = b.booking_id
JOIN booking_leg AS bl
  ON b.booking_id = bl.booking_id
JOIN flight AS f
  ON bl.flight_id = f.flight_id
JOIN airport AS a_dep
  ON f.departure_airport = a_dep.airport_code
JOIN airport AS a_arr
  ON f.arrival_airport = a_arr.airport_code
LEFT JOIN boarding_pass AS bp
  ON bl.booking_leg_id = bp.booking_leg_id
WHERE f.departure_airport = 'DAC'
  AND a_arr.iso_country = 'BD'
  AND bp.pass_id IS NULL
ORDER BY p.passenger_id
LIMIT 200;


--
\echo
\echo Query #4
--
-- For each airport, find the percentage of flights that have departed over 10
-- minutes late. Note that in order to avoid integer division, you must cast at
-- least one of the values to a float. For example: CAST(late_flights AS float)
-- Also, you will need to use the interval data type to represent 10 minutes.
--
-- Schema: departure_airport, percentage (calculated value)
--  Order: departure_airport

SELECT
    f.departure_airport,
    (
      CAST(
        SUM(
          CASE
            WHEN f.actual_departure > f.scheduled_departure + INTERVAL '10 minutes'
            THEN 1 ELSE 0
          END
        ) AS float
      ) / COUNT(*)
    ) * 100 AS percentage
FROM flight AS f
GROUP BY f.departure_airport
ORDER BY f.departure_airport
LIMIT 200;


-- -----------------------------------------------------------------------------
-- Connect to jmudb database
\c jmudb
-- -----------------------------------------------------------------------------

--
\echo
\echo Query #5
--
-- For each subject, how many sections in Fall 2024 were taught with more than
-- 15 students enrolled? Be careful not to count the same section twice!
--
-- Schema: subject, count
--  Order: count (descending), subject

SELECT
    subject,
    COUNT(DISTINCT nbr) AS count
FROM enrollment
WHERE term = 1248 AND enrolled > 15
GROUP BY subject
ORDER BY count DESC, subject
LIMIT 200;


--
\echo
\echo Query #6
--
-- For each instructor, count the total number of students they taught in CS
-- courses over the past three academic years (Summer 2022 to Spring 2025).
--
-- Schema: instructor, students (calculated value)
--  Order: students (descending), instructor

SELECT
    instructor,
    SUM(max_enrolled) AS students
FROM (
    SELECT
        instructor,
        term,
        nbr,
        MAX(enrolled) AS max_enrolled
    FROM enrollment
    WHERE subject = 'CS'
      AND term IN (1225, 1228, 1231, 1235, 1238, 1241, 1245, 1248, 1251)
    GROUP BY instructor, term, nbr
) AS per_course
GROUP BY instructor
ORDER BY students DESC, instructor
LIMIT 200;


--
\echo
\echo Query #7
-- List all sections in Fall 2024 with more that 100 students enrolled, and
-- rank them by course (i.e., the section with the most students is rank #1).
--
-- Schema: subject, number, nbr, enrolled, rank
--  Order: subject, number, nbr

SELECT
  subject,
  number,
  nbr,
  enrolled,
  RANK() OVER (
    PARTITION BY subject, number
    ORDER BY enrolled DESC
  ) AS rank
FROM (
  SELECT
    subject,
    number,
    nbr,
    MAX(enrolled) AS enrolled
  FROM enrollment
  WHERE term = 1248
  GROUP BY subject, number, nbr
) AS fall24
WHERE enrolled > 100
ORDER BY subject, number, nbr;


--
\echo
\echo Query #8
-- Rank departments in Spring 2025 by their total enrollment, i.e., who has the
-- most students enrolled across all sections. (Hint: two nested subqueries)
--
-- Schema: subject, total, rank
--  Order: subject

SELECT
    t1.subject,
    t1.total,
    t1.rank
FROM (
    SELECT
        t2.subject,
        t2.total,
        RANK() OVER (ORDER BY t2.total DESC) AS rank
    FROM (
        SELECT
            subject,
            SUM(max_enrolled) AS total
        FROM (
            SELECT subject, nbr, MAX(enrolled) AS max_enrolled
            FROM enrollment
            WHERE term = 1251
            GROUP BY subject, nbr
        ) AS per_section
        GROUP BY subject
    ) AS t2
) AS t1
ORDER BY t1.subject;

