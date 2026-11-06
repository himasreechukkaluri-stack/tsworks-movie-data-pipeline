import sqlite3

connection = sqlite3.connect("movie_database.db")

with open("schema.sql", "r") as file:
    schema = file.read()

connection.executescript(schema)

connection.close()

print("Database and tables created successfully!")