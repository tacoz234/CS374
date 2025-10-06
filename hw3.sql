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
-- Connect to tpch database
\c tpch
-- -----------------------------------------------------------------------------

--
\echo
\echo Query #1
--
-- Show the customer name, order date, and line items for order number 3.
--
-- Schema: c_name, o_orderdate, l_partkey, l_suppkey, l_quantity, l_extendedPrice
--  Order: l_linenumber

SELECT c.c_name,
       o.o_orderdate,
       l.l_partkey,
       l.l_suppkey,
       l.l_quantity,
       l.l_extendedprice
FROM customer AS c
JOIN orders AS o
  ON o.o_custkey = c.c_custkey
JOIN lineitem AS l
  ON l.l_orderkey = o.o_orderkey
WHERE o.o_orderkey = 3
ORDER BY l.l_linenumber;


--
\echo
\echo Query #2
--
-- Show the part name, supply cost, and retail price of each line item.
--
-- Schema: l_orderkey, l_partkey, l_suppkey, p_name, ps_supplycost, p_retailprice
--  Order: l_orderkey, l_linenumber

SELECT l.l_orderkey,
       l.l_partkey,
       l.l_suppkey,
       p.p_name,
       ps.ps_supplycost,
       p.p_retailprice
FROM lineitem AS l
JOIN part AS p
  ON p.p_partkey = l.l_partkey
JOIN partsupp AS ps
  ON ps.ps_partkey = l.l_partkey
 AND ps.ps_suppkey = l.l_suppkey
ORDER BY l.l_orderkey, l.l_linenumber
LIMIT 200;


--
\echo
\echo Query #3
--
-- Which customers with an account balance over 5000 have no orders?
--
-- Schema: c_name, c_acctbal
--  Order: c_custkey

SELECT c.c_name, c.c_acctbal
FROM customer AS c
LEFT JOIN orders AS o
  ON o.o_custkey = c.c_custkey
WHERE c.c_acctbal > 5000
  AND o.o_orderkey IS NULL
ORDER BY c.c_custkey
LIMIT 200;


--
\echo
\echo Query #4
--
-- Which urgent priority orders have only one line item?
--
-- Schema: o_orderkey, o_custkey, o_orderstatus
--  Order: o_orderkey

SELECT o.o_orderkey, o.o_custkey, o.o_orderstatus
FROM orders AS o
JOIN (
    SELECT l_orderkey
    FROM lineitem
    GROUP BY l_orderkey
    HAVING COUNT(*) = 1
) AS one
  ON one.l_orderkey = o.o_orderkey
WHERE o.o_orderpriority = '1-URGENT'
ORDER BY o.o_orderkey
LIMIT 200;


--
\echo
\echo Query #5
--
-- What parts containing the word "chocolate" were ordered on or after
-- August 1, 1998 and shipped by mail?
--
-- Schema: p_name, ps_supplycost, l_quantity
--  Order: p_partkey

SELECT p.p_name, ps.ps_supplycost, l.l_quantity
FROM lineitem AS l
JOIN orders AS o
  ON o.o_orderkey = l.l_orderkey
JOIN part AS p
  ON p.p_partkey = l.l_partkey
JOIN partsupp AS ps
  ON ps.ps_partkey = l.l_partkey
 AND ps.ps_suppkey = l.l_suppkey
WHERE p.p_name ILIKE '%chocolate%'
  AND o.o_orderdate >= DATE '1998-08-01'
  AND l.l_shipmode = 'MAIL'
ORDER BY p.p_partkey;


--
\echo
\echo Query #6
--
-- Get the min, max, and average supply cost of each part. The average supply cost
-- must be rounded to 2 decimal places.
--
-- Schema: p_name, p_retailprice, min_supplycost, max_supplycost, avg_supplycost
--  Order: p_partkey

SELECT p.p_name,
       p.p_retailprice,
       MIN(ps.ps_supplycost) AS min_supplycost,
       MAX(ps.ps_supplycost) AS max_supplycost,
       ROUND(AVG(ps.ps_supplycost)::numeric, 2) AS avg_supplycost
FROM part AS p
JOIN partsupp AS ps
  ON ps.ps_partkey = p.p_partkey
GROUP BY p.p_partkey, p.p_name, p.p_retailprice
ORDER BY p.p_partkey
LIMIT 200;


--
\echo
\echo Query #7
--
-- What suppliers have an inventory (total available quantity) of over 125,000
-- parts with size over 40.
--
-- Schema: r_name, n_name, s_name, total_qty
--  Order: r_name, n_name, s_name

SELECT r.r_name,
       n.n_name,
       s.s_name,
       SUM(ps.ps_availqty) AS total_qty
FROM supplier AS s
JOIN nation AS n
  ON n.n_nationkey = s.s_nationkey
JOIN region AS r
  ON r.r_regionkey = n.n_regionkey
JOIN partsupp AS ps
  ON ps.ps_suppkey = s.s_suppkey
JOIN part AS p
  ON p.p_partkey = ps.ps_partkey
WHERE p.p_size > 40
GROUP BY r.r_name, n.n_name, s.s_name
HAVING SUM(ps.ps_availqty) > 125000
ORDER BY r.r_name, n.n_name, s.s_name;


--
\echo
\echo Query #8
--
-- Find orders with a total profit of over $375,000. The profit of a single
-- lineitem is defined as quantity * (retail price - supply cost). The profit
-- of an order is the sum of its lineitem profits. For each order, show also
-- the number of lineitems, the total quantity of items (rounded to 0 decimal
-- places), and the total profit of the order (rounded to 2 decimal places).
--
-- Schema: l_orderkey, num_lineitems, total_quantity, total_profit
--  Order: total_profit (descending), total_quantity

SELECT l.l_orderkey,
       COUNT(*) AS num_lineitems,
       ROUND(SUM(l.l_quantity)) AS total_quantity,
       ROUND(SUM(l.l_quantity * (p.p_retailprice - ps.ps_supplycost))::numeric, 2) AS total_profit
FROM lineitem AS l
JOIN part AS p
  ON p.p_partkey = l.l_partkey
JOIN partsupp AS ps
  ON ps.ps_partkey = l.l_partkey
 AND ps.ps_suppkey = l.l_suppkey
GROUP BY l.l_orderkey
HAVING SUM(l.l_quantity * (p.p_retailprice - ps.ps_supplycost)) > 375000
ORDER BY total_profit DESC, total_quantity;

