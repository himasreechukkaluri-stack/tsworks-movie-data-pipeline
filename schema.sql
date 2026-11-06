
PRAGMA foreign_keys = ON;

-- 1. Movies table
CREATE TABLE IF NOT EXISTS movies (
    movie_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    release_year INTEGER,
    decade INTEGER,
    imdb_id TEXT UNIQUE,
    director TEXT,
    plot TEXT,
    box_office TEXT
);

-- 2. Genres table
CREATE TABLE IF NOT EXISTS genres (
    genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    genre_name TEXT NOT NULL UNIQUE
);

-- 3. Movie and Genre relationship
CREATE TABLE IF NOT EXISTS movie_genres (
    movie_id INTEGER,
    genre_id INTEGER,

    PRIMARY KEY (movie_id, genre_id),

    FOREIGN KEY (movie_id)
        REFERENCES movies(movie_id),

    FOREIGN KEY (genre_id)
        REFERENCES genres(genre_id)
);

-- 4. Ratings table
CREATE TABLE IF NOT EXISTS ratings (
    rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    rating REAL NOT NULL CHECK(rating >= 0.5 AND rating <= 5.0),
    rated_at TEXT,

    UNIQUE(user_id, movie_id),

    FOREIGN KEY (movie_id)
        REFERENCES movies(movie_id)
);

-- Indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_ratings_movie
ON ratings(movie_id);

CREATE INDEX IF NOT EXISTS idx_ratings_user
ON ratings(user_id);
