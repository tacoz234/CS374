"""Analyze SOL test pass rates and other results provided by VDOE.

Author: Cole Determan
Version: 9/2/2025
"""

import csv
import sqlite3

# DO NOT EDIT THESE VARIABLES; use them in your functions.
# Connect to the SQLite database file and create a cursor.
con = sqlite3.connect("vdoe.db")
cur = con.cursor()


# TODO add your functions here (see the lab instructions)
def create_tables():
    cur.execute("DROP TABLE IF EXISTS participation")
    cur.execute("DROP TABLE IF EXISTS test_results")
    cur.execute("""CREATE TABLE participation (
    div_num integer,
    div_name text,
    sch_num integer,
    sch_name text,
    sch_type text,
    low_grade text,
    high_grade text,
    subject text,
    subgroup text,
    number_tested integer,
    number_students integer,
    part_rate_2324 real
    )""")
    con.commit()
    cur.execute("""CREATE TABLE test_results (
    div_num integer,
    div_name text,
    sch_num integer,
    sch_name text,
    sch_type text,
    low_grade text,
    high_grade text,
    subject text,
    grade_level text,
    test_name text,
    pass_rate_2122 integer,
    pass_rate_2223 integer,
    pass_rate_2324 integer,
    adv_rate_2122 integer,
    adv_rate_2223 integer,
    adv_rate_2324 integer
    )""")
    con.commit()

def import_data():
    with open("School-Participation_rates_23_24.csv", newline="") as file:
        reader = csv.reader(file)
        next(reader)  # skip header row
        for row in reader:
            cur.execute("INSERT INTO participation "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)
    con.commit()

    with open("School_Test_by_level_2023_2024.csv", newline="") as file:
        reader = csv.reader(file)
        next(reader)  # skip header row
        for row in reader:
            cur.execute("INSERT INTO test_results "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)
    con.commit()

def query_school(div_num, sch_num):
    # Query the participation rates
    res = cur.execute("""
        SELECT div_name, sch_name, subject, number_tested, number_students
        FROM participation
        WHERE div_num = ?
            AND sch_num = ?
            AND subgroup = 'All Students'
        """, (div_num, sch_num))
    data = res.fetchall()
    print()
    print(f"Results for {data[0][1]}, {data[0][0]}")
    print()
    for row in data:
        print(f"Subject: {row[2]}, Tested: {row[3]}/{row[4]}")
    
    # Query the SOL test pass rates
    res2 = cur.execute("""
        SELECT subject, grade_level, test_name, pass_rate_2324
        FROM test_results
        WHERE div_num = ?
            AND sch_num = ?
        """, (div_num, sch_num))
    test_data = res2.fetchall()
    print()
    for row in test_data:
        if row[3] is not None and row[3] != "<":
            print(f"{row[0]}, {row[1]}, {row[2]}, 2023-24 Pass Rate: {row[3]}")
    print()

def update_school(div_num, sch_num):
    print("Hacking database...", end="")
    cur.execute("""
        UPDATE test_results 
        SET pass_rate_2324 = 100, adv_rate_2324 = 100
        WHERE div_num = ? AND sch_num = ?
        """, (div_num, sch_num))
    con.commit()
    print("success!\nHave a nice day.")


if __name__ == "__main__":
    create_tables()
    import_data()
    div_num = input("Enter division number: ")
    sch_num = input("Enter school number: ")
    query_school(div_num, sch_num)
    update_school(div_num, sch_num)