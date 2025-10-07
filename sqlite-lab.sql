-- Cole Determan

SELECT *
FROM title
WHERE title = 'The Wanker'

SELECT *
FROM person
WHERE name = 'Jim Carrey'

SELECT *
FROM aka
WHERE aka = 'Moana 2'
  AND language = 'fr'

SELECT *
FROM title 
 JOIN castcrew USING (tid)
  JOIN person USING (pid)
WHERE pid = 120

SELECT *
FROM person
WHERE birth = '2003'
LIMIT 10
ORDER BY name

SELECT *
FROM aka
WHERE aka = 'Moana'