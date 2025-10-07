--
-- Name: Cole Determan
--
-- Write your queries below each comment. Please use good style (one clause
-- per line, JOIN syntax, indentation) and make sure all queries end with a
-- semicolon. When necessary, limit the output to the first 200 results.
--
-- DO NOT MODIFY OR DELETE ANY OTHER LINES!
--

.headers on
.mode tabs

-- ------------------------------------------------------------------------------
-- Part 1: Employees Database
-- ------------------------------------------------------------------------------

--
.print "\nQuery #1"
--
-- Show the names and dates hired of all employees who were a manager
-- at some point.
--
-- Schema: dept_name, first_name, last_name, hire_date
--  Order: dept_name, last_name, first_name
select dept_name, first_name, last_name, hire_date
from dept_manager
join departments using (dept_no)
join employees using (emp_no)
order by dept_name, last_name, first_name;

--
.print "\nQuery #2"
--
-- For each department, list the total number of employees who have
-- worked at any time.
--
-- Schema: dept_name, emp_count
--  Order: dept_name
select dept_name, count(emp_no) as emp_count
from departments
join dept_emp using (dept_no)
group by dept_name
order by dept_name;

--
.print "\nQuery #3"
--
-- List all employees who worked in the Research department on
-- November 20, 1985 (the day that Microsoft Windows launched)
-- and who were born before the year 1960.
--
-- Schema: emp_no, from_date, to_date, birth_date, first_name, last_name
--  Order: emp_no
select emp_no, from_date, to_date, birth_date, first_name, last_name
from employees
join dept_emp using (emp_no)
join departments using (dept_no)
where dept_name = 'Research'
  and from_date <= '1985-11-20'
  and to_date >= '1985-11-20'
  and birth_date < '1960-01-01'
order by emp_no
limit 200;

--
.print "\nQuery #4"
--
-- List all employees who ever worked for the Development department
-- as Engineers or Senior Engineers.
--
-- Schema: emp_no, first_name, last_name, gender, title
--  Order: emp_no
select emp_no, first_name, last_name, gender, title
from employees
join dept_emp using (emp_no)
join departments using (dept_no)
join titles using (emp_no)
where dept_name = 'Development'
  and (title = 'Engineer' or title = 'Senior Engineer')
order by emp_no, title
limit 200;

-- ------------------------------------------------------------------------------
-- Part 2: World Database
-- ------------------------------------------------------------------------------

--
.print "\nQuery #5"
--
-- What cities in the database have a population over 3 million?
--
-- Schema: Population, CityName, District, CountryName, Continent
--  Order: Population
select city.Population, city.Name as CityName, District, country.Name as CountryName, Continent
from city
join country on city.CountryCode = country.Code
where city.Population > 3000000
order by city.Population
limit 200;

--
.print "\nQuery #6"
--
-- Which countries have the majority (over half) of their population
-- living in the capital city?
--
-- Schema: CityName, CityPopulation, CountryName, CountryPopulation
--  Order: CountryName, CityName
select city.Name as CityName, city.Population as CityPopulation, country.Name as CountryName, country.Population as CountryPopulation
from city
join country on city.CountryCode = country.Code
where city.ID = country.Capital
  and city.Population > (country.Population / 2.0)
order by CountryName, CityName;

--
.print "\nQuery #7"
--
-- Which countries have Spanish as an official language? Also calculate
-- the number of Spanish speakers by multiplying the population and the
-- percentage, rounded to the nearest integer.
--
-- Schema: Name, LocalName, Region, Population, Percentage, Speakers
--  Order: Speakers
select country.Name, LocalName, Region, country.Population, Percentage, round(country.Population * Percentage / 100.0) as Speakers
from country
join countrylanguage on country.Code = countrylanguage.CountryCode
where Language = 'Spanish'
  and IsOfficial = 'T'
order by Speakers;

--
.print "\nQuery #8"
--
-- How many languages are spoken in each country? The count should
-- include both official and unofficial languages.
--
-- Schema: Name, Region, Languages
--  Order: Languages (descending), Name (ascending)
select Name, Region, count(Language) as Languages
from country
join countrylanguage on country.Code = countrylanguage.CountryCode
group by country.Code, Name, Region
order by Languages desc, Name asc
limit 200;