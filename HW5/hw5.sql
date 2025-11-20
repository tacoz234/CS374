--
-- Name: TYPE YOUR NAME HERE
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


--
\echo
\echo Query #2
--
-- Show the passengers who have flown out of Dulles (IAD) but have never flown
-- out of Orlando (MCO).
--
-- Schema: passenger_id, first_name, last_name
--  Order: passenger_id


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


--
\echo
\echo Query #6
--
-- For each instructor, count the total number of students they taught in CS
-- courses over the past three academic years (Summer 2022 to Spring 2025).
--
-- Schema: instructor, students (calculated value)
--  Order: students (descending), instructor


--
\echo
\echo Query #7
-- List all sections in Fall 2024 with more that 100 students enrolled, and
-- rank them by course (i.e., the section with the most students is rank #1).
--
-- Schema: subject, number, nbr, enrolled, rank
--  Order: subject, number, nbr


--
\echo
\echo Query #8
-- Rank departments in Spring 2025 by their total enrollment, i.e., who has the
-- most students enrolled across all sections. (Hint: two nested subqueries)
--
-- Schema: subject, total, rank
--  Order: subject

