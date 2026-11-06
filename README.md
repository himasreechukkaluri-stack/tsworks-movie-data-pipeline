# Movie Data Pipeline

## Project Overview

This project implements a simple ETL (Extract, Transform, Load) pipeline using the MovieLens Latest Small dataset and the OMDb API.

The pipeline extracts movie and rating data, cleans and transforms it, enriches movie information using the OMDb API, and stores the processed data in an SQLite database.

## Technologies Used

- Python
- Pandas
- Requests
- SQLite
- SQL
- SQLAlchemy
- OMDb API
- Python-dotenv

## Dataset

Source: [MovieLens Latest Small Dataset](https://grouplens.org/datasets/movielens/latest/)

The dataset contains:
- movies.csv
- ratings.csv

## Project Structure

```text
movie-data-pipeline/
│
├── data/
│   ├── movies.csv
│   ├── ratings.csv
│   └── api_cache.json
│
├── venv/
├── etl.py
├── schema.sql
├── create_db.py
├── run_queries.py
├── queries.sql
├── test_api.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
└── movie_database.db
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd movie-data-pipeline
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the OMDb API key

Create a `.env` file in the project directory:

```text
OMDB_API_KEY=your_api_key
```

Get an API key from [OMDb API](https://www.omdbapi.com/apikey.aspx).

### 6. Create the database

```bash
python create_db.py
```

### 7. Run the ETL pipeline

```bash
python etl.py
```

### 8. Execute analytical queries

```bash
python run_queries.py
```

## Database Tables

- **movies:** Stores movie details and OMDb information.
- **genres:** Stores unique movie genres.
- **movie_genres:** Maintains the relationship between movies and genres.
- **ratings:** Stores user ratings and timestamps.

## Analytical Queries

The project answers the following questions:

1. Which movie has the highest average rating?
2. What are the top 5 genres based on average rating?
3. Which director has directed the most movies?
4. What is the average rating for each release year?

## ETL Features

- Data extraction from CSV files.
- Data cleaning and transformation using Pandas.
- Movie information enrichment using OMDb API.
- API response caching to reduce repeated requests.
- SQLite database integration.
- Handling missing API information and request errors.
- Batch processing of movie records.
- Prevention of duplicate records through database constraints and upsert operations.

## Current Dataset Processing Results

| Component | Records |
|---|---:|
| Movies | 9,742 |
| Genres | 19 |
| Movie-genre relationships | 22,050 |
| Ratings | 100,836 |
| Cached API responses | 570 |

## Author

Himasree Chukkaluri