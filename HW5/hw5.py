"""Autograder for Postgres queries assignment.

Author: CS374 Faculty
Version: 11/13/2025
"""

import difflib
import psycopg
import re
import socket

# The expected number of queries on this assignment
QUERIES = 8

# Determine whether connecting from on/off campus
try:
    socket.gethostbyname("data.cs.jmu.edu")
    HOST = "data.cs.jmu.edu"
except socket.gaierror:
    HOST = "localhost"


def connect(dbname):
    """Connect to the database and create a cursor.

    Args:
        dbname: The name of the database to use.
    """
    global con, cur
    con = psycopg.connect(host=HOST, user="demo", password="demo", dbname=dbname)
    cur = con.cursor()


def assert_eq(actual, expect, message=""):
    """Assert whether two values are equal (custom feedback).

    Args:
        actual: The value produced by the code being tested.
        expect: The expected value to compare with `actual`.
        message: Text to display if AssertionError is raised.

    Raises:
        AssertionError: If `actual` is not equal to `expect`,
                        with a message displaying both values.
    """
    if type(actual) is str:
        # Abbreviate output if too long
        a_str = actual if len(actual) <= 120 else actual[:120] + "..."
        e_str = expect if len(expect) <= 120 else expect[:120] + "..."
    else:
        # Convert to simple strings
        a_str = str(actual)
        e_str = str(expect)

    assert actual == expect, f"{message}\n  Actual: {a_str}\n  Expect: {e_str}"


def res2str(res):
    """Convert query results into a multiline string.

    Args:
        res (list of tuples): Results obtained from fetchall().

    Returns:
        str: Each line is one row with values separated by tabs.
    """
    return "\n".join(
        ["\t".join(map(lambda x: "" if x is None else str(x), tup)) for tup in res]
    )


def run_query(sql, txt, qno):
    """Run the query and compare with expected output.

    Args:
        sql (str): The sql chunk from the HW file.
        txt (str): The expected output of the sql.
        qno (int): The query number being tested.

    Raises:
        RuntimeError: If incorrect number of queries.
    """

    # Print status message for autograder feedback
    if qno:
        print(f"Running Query #{qno}...")
        # Reset connection in case of previous error or timeout
        con.cancel_safe()
        connect(con.info.dbname)
    elif "\\c" in sql:
        beg = sql.find("\\c")
        end = sql.find("\n", beg)
        dbname = sql[beg + 3 : end]
        print("Connecting to", dbname)
        connect(dbname)
        return
    else:
        print("Running header comment")
        connect("postgres")

    # Execute the chunk, convert results to text
    results = []
    if "\\echo" in sql:
        sql = sql.replace("\\echo", "--\\echo")
        beg = sql.find("\\echo")
        end = sql.find("\n", beg)
        name = sql[beg + 6 : end]
        results.append(name)
    res = cur.execute(sql)
    if res.rowcount > -1:
        column_names = [desc[0] for desc in res.description]
        schema = "\t".join(column_names)
        output = res2str(res.fetchall())
        output = output.replace(".0\n", "\n")  # integer hack
        footer = f"({res.rowcount} rows)\n"
        results.append(schema + "\n" + output + "\n" + footer)

    # Compare with expected output, if applicable
    if txt:
        if len(results) == 0:
            raise RuntimeError(f"Missing output of \\echo Query #{qno}")

        # 1st line blank, 2nd line "Query #"
        actual = results[0]
        expect = txt.splitlines()
        assert_eq(actual, expect[1], "Incorrect query number")

        # Check the number of queries run
        if len(results) == 1:
            raise RuntimeError("No results (code is blank)")
        if len(results) > 2:
            raise RuntimeError("Extra results (more than one query)")

        # Calculate similarity percentage
        actual = "\n" + results[0] + "\n" + results[1]
        seq = difflib.SequenceMatcher(None, actual, txt)
        sim = int(seq.ratio() * 100)
        print(f"Output matches {sim}%")

        # Compare schema and row count
        actual = results[1].rstrip().splitlines()
        expect = expect[2:]
        assert_eq(actual[0], expect[0], "Incorrect schema")
        a_rows = len(actual) - 2
        e_rows = len(expect) - 2
        assert_eq(a_rows, e_rows, "Incorrect row count")

        # Compare each row of the results
        for i in range(1, a_rows):
            assert_eq(actual[i], expect[i], f"Row {i} does not match")

    # No output expected (not a SELECT)
    elif results:
        raise RuntimeError(f"Results should be empty: {results}")


def split_file(path):
    """Split a text file into chunks by query number.

    Args:
        path (str): The path of the text file to split.

    Returns:
        list of str: The code or output for each query.
    """

    # Read the file contents
    beg = 0
    chunks = []
    with open(path) as file:
        text = file.read()

    # Extract the text before each query
    pattern = re.compile(r"^-- -+\n-- |^(--)?\n?.*Query #\d+", re.MULTILINE)
    for match in re.finditer(pattern, text):
        end = match.start()
        chunks.append(text[beg:end])
        beg = end

    # Append the text of the final query
    chunks.append(text[beg:])
    return chunks


def main(sql_file, txt_file, g_scope=False):
    """Split the given files and execute each query.

    Args:
        sql_file (str): Path to the sql script file.
        txt_file (str): Path to the expected output.
        g_scope (bool): True if running on Gradescope.

    Returns:
        tuple or None: queries and outputs (for Gradescope)

    Raises:
        RuntimeError: If a file doesn't split correctly.
    """

    # Split and validate the given files
    queries = split_file(sql_file)
    q_count = sum(1 for s in queries if "Query #" in s)
    if q_count != QUERIES:
        raise RuntimeError(f"Expected {QUERIES} queries, but {q_count} were found.")
    outputs = split_file(txt_file)
    del outputs[0]  # Blank string
    o_count = sum(1 for s in outputs if "Query #" in s)
    if o_count != QUERIES:
        raise RuntimeError(f"Expected {QUERIES} outputs, but {o_count} were found.")

    # Gradescope skips the rest of main()
    if g_scope:
        return queries, outputs

    # Execute each chunk of sql in order
    qno = 0
    for sql in queries:
        try:
            if "Query #" in sql:
                qno += 1
                run_query(sql, outputs[qno-1], qno)
            else:
                run_query(sql, None, None)  # Ex: meta-command
        except Exception as e:
            # Assertion or psycopg or Runtime error
            print(type(e).__name__ + ":", e)
        print()

    # That's all folks!
    if qno != QUERIES:
        print(f"Error: Something went wrong. {qno} of {QUERIES} queries were run.")


if __name__ == "__main__":
    main("hw5.sql", "hw5-sol.txt")
