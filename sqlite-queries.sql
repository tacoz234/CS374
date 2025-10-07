--Cole Determan
--Find the current manager of each department
-- Schema: dept_name, first_name, last_name
-- Order: dept_name

select dept_name, first_name, last_name
from dept_manager
join departments using (dept_no)
join employees using (emp_no)
where to_date = "9999-01-01"
order by dept_name

-- Show the current department of a specific employee
-- Schema: first_name, last_name, dept_name
-- Order: N/A
select first_name, last_name, dept_name
from employees
join dept_emp using (emp_no)
join departments using (dept_no)
where to_date = "9999-01-01"

-- Top 10 highest paid employees (current salary only)
-- Schema: emp_no, first_name, last_name, salary
-- Order: salary (descending)
select emp_no, first_name, last_name, salary
from employees
join salaries using (emp_no)
where to_date = "9999-01-01"
order by salary desc
limit 10

-- List all countries in Europe with their population.
-- Schema: ID, Name, Population
-- Order: Population (descending)
select Code, Name, Population
from country
where Continent = "Europe"
order by Population desc

-- Find the capital city of Finland.
-- Schema: Country, Capital_City
-- Order: N/A
select country.Name, city.Name
from country
join city on country.code = city.CountryCode
where country.Name = "Finland"
and Capital = ID
