"""Practice connecting to PostgreSQL and creating tables with fake data.

Author: Cole Determan
Version: [Current Date]
"""

import psycopg
import random
from faker import Faker

# Database connection string

CONNSTR = "host=localhost port=5432 dbname=sec1 user=PGUSER password=PGPASSWORD"

# Initialize Faker for generating fake data
fake = Faker()


def create_tables():
    """Create the superheroes and supervillains tables in PostgreSQL.
    
    Recreates the same table structure from HW2 but adapted for PostgreSQL.
    """
    try:
        with psycopg.connect(CONNSTR) as conn:
            with conn.cursor() as cur:
                # Drop tables if they exist (for clean recreation)
                cur.execute("DROP TABLE IF EXISTS supervillains CASCADE")
                cur.execute("DROP TABLE IF EXISTS superheroes CASCADE")
                
                # Create superheroes table
                cur.execute("""
                CREATE TABLE superheroes (
                    id SERIAL PRIMARY KEY,
                    hero_name TEXT NOT NULL,
                    secret_identity TEXT NOT NULL,
                    age REAL NOT NULL,
                    height REAL NOT NULL,
                    nick_name TEXT NOT NULL
                )""")
                
                # Create supervillains table with foreign key
                cur.execute("""
                CREATE TABLE supervillains (
                    id SERIAL PRIMARY KEY,
                    villain_name TEXT NOT NULL,
                    age REAL NOT NULL,
                    height REAL NOT NULL,
                    main_hero_id INTEGER NOT NULL,
                    FOREIGN KEY (main_hero_id) REFERENCES superheroes(id)
                )""")
                
                conn.commit()
                print("Tables created successfully!")
                
    except psycopg.Error as e:
        print(f"Error creating tables: {e}")


def generate_hero_data():
    """Generate fake data for the superheroes table.
    
    Returns:
        list: A list of lists containing 20 rows of superhero data.
    """
    heroes_data = []
    
    # Predefined superhero names and nicknames for more realistic data
    hero_names = [
        "Captain Thunder", "Shadow Walker", "Iron Guardian", "Flame Phoenix", "Ice Storm",
        "Lightning Bolt", "Steel Titan", "Wind Rider", "Earth Shaker", "Mind Reader",
        "Time Keeper", "Space Ranger", "Night Crawler", "Sun Warrior", "Moon Guardian",
        "Star Fighter", "Ocean Master", "Forest Protector", "Sky Defender", "Crystal Sage"
    ]
    
    nicknames = [
        "The Thunderous One", "Master of Shadows", "The Iron Will", "Phoenix Rising", "Frozen Justice",
        "The Lightning Strike", "Titanium Heart", "Wind's Fury", "Earth's Might", "The Mind's Eye",
        "Keeper of Time", "Guardian of Space", "Night's Shadow", "Solar Flare", "Lunar Light",
        "Stellar Force", "Ocean's Depth", "Nature's Wrath", "Sky's Limit", "Crystal Clear"
    ]
    
    for i in range(20):
        hero_data = [
            hero_names[i],  # hero_name
            fake.name(),    # secret_identity
            round(random.uniform(25.0, 95.0), 1),  # age (years since first appearance)
            round(random.uniform(1.60, 2.10), 2),  # height in meters
            nicknames[i]    # nick_name
        ]
        heroes_data.append(hero_data)
    
    return heroes_data


def generate_villain_data():
    """Generate fake data for the supervillains table.
    
    Returns:
        list: A list of lists containing villain data (one villain per hero).
    """
    villains_data = []
    
    # Predefined villain names
    villain_names = [
        "Dr. Chaos", "Shadow Fiend", "Metal Menace", "Inferno King", "Frost Bite",
        "Storm Breaker", "Iron Fist", "Tornado Terror", "Quake Master", "Brain Drain",
        "Time Thief", "Void Walker", "Dark Creeper", "Solar Flare", "Eclipse",
        "Black Hole", "Tsunami", "Thorn King", "Cloud Crusher", "Shard Master"
    ]
    
    for i in range(20):
        villain_data = [
            villain_names[i],  # villain_name
            round(random.uniform(30.0, 100.0), 1),  # age
            round(random.uniform(1.65, 2.05), 2),   # height in meters
            i + 1  # main_hero_id (references the hero's id)
        ]
        villains_data.append(villain_data)
    
    return villains_data


def insert_table1(heroes_data):
    """Insert hero data into the superheroes table.
    
    Args:
        heroes_data (list): List of lists containing hero data.
    """
    try:
        with psycopg.connect(CONNSTR) as conn:
            with conn.cursor() as cur:
                # Insert all hero data
                cur.executemany("""
                INSERT INTO superheroes (hero_name, secret_identity, age, height, nick_name)
                VALUES (%s, %s, %s, %s, %s)
                """, heroes_data)
                
                conn.commit()
                print(f"Successfully inserted {len(heroes_data)} heroes into the database!")
                
    except psycopg.Error as e:
        print(f"Error inserting hero data: {e}")


def insert_table2(villains_data):
    """Insert villain data into the supervillains table.
    
    Args:
        villains_data (list): List of lists containing villain data.
    """
    try:
        with psycopg.connect(CONNSTR) as conn:
            with conn.cursor() as cur:
                # Insert all villain data
                cur.executemany("""
                INSERT INTO supervillains (villain_name, age, height, main_hero_id)
                VALUES (%s, %s, %s, %s)
                """, villains_data)
                
                conn.commit()
                print(f"Successfully inserted {len(villains_data)} villains into the database!")
                
    except psycopg.Error as e:
        print(f"Error inserting villain data: {e}")


if __name__ == "__main__":
    # Create the tables
    create_tables()
    
    # Generate fake data
    print("\nGenerating fake data...")
    heroes_data = generate_hero_data()
    villains_data = generate_villain_data()
    
    # Print the generated data to check it
    print("\nGenerated Heroes Data:")
    for i, hero in enumerate(heroes_data, 1):
        print(f"{i}: {hero}")
    
    print("\nGenerated Villains Data:")
    for i, villain in enumerate(villains_data, 1):
        print(f"{i}: {villain}")
    
    # Insert the fake data
    print("\nInserting data into database...")
    insert_table1(heroes_data)
    insert_table2(villains_data)
    
    print("\nAll operations completed! Check pgAdmin to verify the data was inserted correctly.")