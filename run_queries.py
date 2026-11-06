
import sqlite3

connection = sqlite3.connect("movie_database.db")
cursor = connection.cursor()

with open("queries.sql", "r") as file:
    queries = file.read()

query_list = queries.split(";")

for index, query in enumerate(query_list, start=1):

    if query.strip():

        print("\nQUERY", index)
        print("-" * 50)

        cursor.execute(query)

        columns = [description[0] for description in cursor.description]

        print(columns)

        for row in cursor.fetchall():
            print(row)

connection.close()
