
import pandas as pd
import sqlite3
import os
import requests
import time
import json
from dotenv import load_dotenv

# ----------------------------------
# 1. Load API key
# ----------------------------------

load_dotenv()
API_KEY = os.getenv("OMDB_API_KEY")

# ----------------------------------
# 2. Load CSV files
# ----------------------------------

movies = pd.read_csv("data/movies.csv")
ratings = pd.read_csv("data/ratings.csv")

print("Movies loaded:", len(movies))
print("Ratings loaded:", len(ratings))

# ----------------------------------
# 3. Load API cache
# ----------------------------------

cache_file = "data/api_cache.json"

if os.path.exists(cache_file):
    with open(cache_file, "r") as file:
        api_cache = json.load(file)
else:
    api_cache = {}

print("Existing cached movies:", len(api_cache))

# ----------------------------------
# 4. Clean movie data
# ----------------------------------

movies["release_year"] = movies["title"].str.extract(
    r"\((\d{4})\)"
)

movies["release_year"] = pd.to_numeric(
    movies["release_year"], errors="coerce"
).astype("Int64")

movies["title"] = movies["title"].str.replace(
    r"\s*\(\d{4}\)$", "", regex=True
)

print("\nCleaned Movie Data:")
print(movies[["movieId", "title", "release_year"]].head(10))

print("\nMissing Release Years:",
      movies["release_year"].isnull().sum())

# ----------------------------------
# 5. Clean genre data
# ----------------------------------

genre_data = movies[["movieId", "genres"]].copy()

genre_data["genres"] = genre_data["genres"].str.split("|")

genre_data = genre_data.explode("genres")

genre_data["genres"] = genre_data["genres"].str.strip()

genre_data = genre_data[
    genre_data["genres"] != "(no genres listed)"
]

print("\nTotal Genre Records:", len(genre_data))

print("\nUnique Genres:")
print(genre_data["genres"].unique())

# ----------------------------------
# 6. Clean ratings data
# ----------------------------------

ratings = ratings.drop_duplicates()

ratings["timestamp"] = pd.to_datetime(
    ratings["timestamp"], unit="s"
)

ratings = ratings.rename(columns={
    "userId": "user_id",
    "movieId": "movie_id",
    "timestamp": "rated_at"
})

print("\nCleaned Ratings:")
print(ratings.head())

print("\nRatings Shape:", ratings.shape)

print("\nMissing Values:")
print(ratings.isnull().sum())

# ----------------------------------
# 7. OMDb API function
# ----------------------------------

def get_movie_details(movie_id, title, year):

    cache_key = str(movie_id)

    if cache_key in api_cache:
        return api_cache[cache_key]

    params = {
        "apikey": API_KEY,
        "t": title
    }

    if pd.notna(year):
        params["y"] = int(year)

    try:
        response = requests.get(
            "https://www.omdbapi.com/",
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        api_cache[cache_key] = data

        with open(cache_file, "w") as file:
            json.dump(api_cache, file, indent=4)

        if data.get("Response") == "True":
            return data

        print("Movie not found:", title)
        return None

    except requests.exceptions.RequestException as error:
        print("API Request Error:", error)

    except ValueError as error:
        print("Invalid API response:", error)

    return None

# ----------------------------------
# 8. Test OMDb API
# ----------------------------------

first_movie = movies.iloc[0]

movie_details = get_movie_details(
    first_movie["movieId"],
    first_movie["title"],
    first_movie["release_year"]
)

print("\nOMDb Movie Details:")

if movie_details:
    print("Title:", movie_details.get("Title"))
    print("Director:", movie_details.get("Director"))
    print("Plot:", movie_details.get("Plot"))
    print("Box Office:", movie_details.get("BoxOffice"))
else:
    print("Movie details not available.")

# ----------------------------------
# 9. Batch processing

# ----------------------------------
# 9. Batch processing
# ----------------------------------

print("\nStarting batch processing...")

# Select movies not already present in cache
uncached_movies = movies[
    ~movies["movieId"].astype(str).isin(api_cache.keys())
]

batch_size = 200

for index, row in uncached_movies.head(batch_size).iterrows():

    details = get_movie_details(
        row["movieId"],
        row["title"],
        row["release_year"]
    )

    if details and details.get("Response") == "True":
        print("Processed:", row["title"])

    time.sleep(0.2)

with open(cache_file, "w") as file:
    json.dump(api_cache, file, indent=4)

print("\nBatch processing completed!")
print("Cached movies:", len(api_cache))

# ----------------------------------
# 10. Connect to SQLite database
# ----------------------------------

connection = sqlite3.connect("movie_database.db")

connection.execute("PRAGMA foreign_keys = ON")

cursor = connection.cursor()

# ----------------------------------
# 11. Load movies into database
# ----------------------------------

movie_records = []

for _, row in movies.iterrows():

    details = api_cache.get(str(row["movieId"]), {})

    if details.get("Response") != "True":
        details = {}

    year = (
        None if pd.isna(row["release_year"])
        else int(row["release_year"])
    )

    decade = None if year is None else (year // 10) * 10

    movie_records.append((
        int(row["movieId"]),
        row["title"],
        year,
        decade,
        details.get("imdbID"),
        details.get("Director"),
        details.get("Plot"),
        details.get("BoxOffice")
    ))

cursor.executemany("""
    INSERT INTO movies
    (movie_id, title, release_year, decade, imdb_id,
     director, plot, box_office)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)

    ON CONFLICT(movie_id) DO UPDATE SET
        title = excluded.title,
        release_year = excluded.release_year,
        decade = excluded.decade,
        imdb_id = excluded.imdb_id,
        director = excluded.director,
        plot = excluded.plot,
        box_office = excluded.box_office
""", movie_records)

connection.commit()

print("\nMovies loaded into database:", len(movie_records))

# ----------------------------------
# 12. Load genres into database
# ----------------------------------

unique_genres = genre_data["genres"].unique()

cursor.executemany(
    "INSERT OR IGNORE INTO genres (genre_name) VALUES (?)",
    [(genre,) for genre in unique_genres]
)

cursor.execute("SELECT genre_id, genre_name FROM genres")

genre_map = {
    name: genre_id
    for genre_id, name in cursor.fetchall()
}

movie_genre_records = []

for _, row in genre_data.iterrows():

    movie_genre_records.append((
        int(row["movieId"]),
        genre_map[row["genres"]]
    ))

cursor.executemany("""
    INSERT OR IGNORE INTO movie_genres
    (movie_id, genre_id)
    VALUES (?, ?)
""", movie_genre_records)

connection.commit()

print("Genres loaded:", len(unique_genres))
print("Movie-genre records processed:", len(movie_genre_records))

# ----------------------------------
# 13. Load ratings into database
# ----------------------------------

rating_records = []

for row in ratings.itertuples(index=False):

    rating_records.append((
        int(row.user_id),
        int(row.movie_id),
        float(row.rating),
        row.rated_at.strftime("%Y-%m-%d %H:%M:%S")
    ))

cursor.executemany("""
    INSERT OR IGNORE INTO ratings
    (user_id, movie_id, rating, rated_at)
    VALUES (?, ?, ?, ?)
""", rating_records)

connection.commit()

print("Ratings processed:", len(rating_records))

# ----------------------------------
# 14. Verify database records
# ----------------------------------

print("\nDatabase Record Counts:")

for table in ["movies", "genres", "movie_genres", "ratings"]:

    cursor.execute(f"SELECT COUNT(*) FROM {table}")

    count = cursor.fetchone()[0]

    print(table, ":", count)

connection.close()

print("\nETL PIPELINE COMPLETED SUCCESSFULLY!")
