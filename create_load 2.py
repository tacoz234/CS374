 
import psycopg
from faker import Faker


CONNSTR = "host=localhost port=5432 dbname=sec1 user=determsc password=113893504"

def create_tables():
    """Create the Superheroes and Supervillains tables."""
    with psycopg.connect(CONNSTR) as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS supervillains;")
            cur.execute("DROP TABLE IF EXISTS superheroes;")

            cur.execute("""
            CREATE TABLE superheroes (
                id INTEGER PRIMARY KEY,
                hero_name TEXT NOT NULL,
                secret_identity TEXT NOT NULL,
                age REAL NOT NULL,
                height REAL NOT NULL,
                nick_name TEXT NOT NULL
            );
            """)

            cur.execute("""
            CREATE TABLE supervillains (
                id INTEGER PRIMARY KEY,
                villain_name TEXT NOT NULL,
                age REAL NOT NULL,
                height REAL NOT NULL,
                main_hero_id INTEGER NOT NULL,
                FOREIGN KEY (main_hero_id) REFERENCES superheroes(id)
            );
            """)

        conn.commit()

def make_fake_heroes(n):
    """Generate fake superhero data."""
    fake = Faker()
    heroes = []
    for i in range(1, n + 1):
        hero_name = f"{fake.color_name()} {fake.word().title()}"
        secret_identity = fake.name()
        age = fake.random_int(min=20, max=100)
        height = round(fake.random.uniform(1.50, 2.10), 2)  # meters
        nick_name = f"The {fake.job().split()[0]}"  # Take first word of job title
        heroes.append([i, hero_name, secret_identity, age, height, nick_name])
    return heroes




def make_fake_villains(heroes):
    """Generate fake supervillains for each hero (1 villain per hero)."""
    fake = Faker()
    villains = []
    for i, hero in enumerate(heroes, start=1):
        hero_id = hero[0]
        villain_name = fake.last_name()
        age = fake.random_int(min=20, max=100)
        height = round(fake.random.uniform(1.50, 2.10), 2)
        villains.append([i, villain_name, age, height, hero_id])
    return villains

def insert_table1(heroes):
    """Insert superhero rows into superheroes."""
    with psycopg.connect(CONNSTR) as conn:
        with conn.cursor() as cur:
            cur.executemany("""
                INSERT INTO superheroes (id, hero_name, secret_identity, age, height, nick_name)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, heroes)
        conn.commit()

def insert_table2(villains):
    """Insert supervillain rows into supervillains."""
    with psycopg.connect(CONNSTR) as conn:
        with conn.cursor() as cur:
            cur.executemany("""
                INSERT INTO supervillains (id, villain_name, age, height, main_hero_id)
                VALUES (%s, %s, %s, %s, %s);
            """, villains)
        conn.commit()

if __name__ == "__main__":
    create_tables()

    heroes = make_fake_heroes(20)
    villains = make_fake_villains(heroes)

    insert_table1(heroes)
    insert_table2(villains)



