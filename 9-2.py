import sqlite3

con = sqlite3.connect("tutorial.db")
cur = con.cursor()

cur.execute("SELECT name FROM sqlite_master")
res.fetchone() # returns ('movie')
# takes first result from answer

cur.execute("""
   INSERT INTO movie VALUES
   ('Monty Python and the Holy Grain', 1975, 8.2),
   ('And Now for Something Completely Different', 1971, 7.5))
   """)
con.commit()

res = cur.execute("SELECT * FROM movie")

res.fetchall()
# returns [('Monty Python and the Holy Grain', 1975, 8.2), ('And Now for Something Completely Different', 1971, 7.5)]

for row in cur:
  print(row)

cur.execute("SELECT * FROM movie WHERE year = ?", (1975,))
cur.fetchall()
# returns [('Monty Python and the Holy Grain', 1975, 8.2)]

data = [
  ('Monty Python Live at the Hollywood Bowl', 1982, 7.9),
  ('Monty Pythons The Meaning of Life', 1983, 7.5),
  ('Monty Pythons Life of Brian', 1979, 8.0),
]

