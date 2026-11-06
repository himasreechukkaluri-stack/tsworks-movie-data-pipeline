-- 1. Highest average-rated movie

SELECT
    m.title,
    ROUND(AVG(r.rating), 2) AS average_rating,
    COUNT(r.rating) AS total_ratings
FROM movies m
JOIN ratings r ON m.movie_id = r.movie_id
GROUP BY m.movie_id, m.title
HAVING COUNT(r.rating) >= 10
ORDER BY average_rating DESC, total_ratings DESC
LIMIT 1;


-- 2. Top 5 genres by average rating

SELECT
    g.genre_name,
    ROUND(AVG(r.rating), 2) AS average_rating
FROM genres g
JOIN movie_genres mg ON g.genre_id = mg.genre_id
JOIN ratings r ON mg.movie_id = r.movie_id
GROUP BY g.genre_id, g.genre_name
ORDER BY average_rating DESC
LIMIT 5;


-- 3. Director with the most movies

SELECT
    director,
    COUNT(*) AS total_movies
FROM movies
WHERE director IS NOT NULL
AND director != 'N/A'
GROUP BY director
ORDER BY total_movies DESC
LIMIT 1;


-- 4. Average rating per release year

SELECT
    m.release_year,
    ROUND(AVG(r.rating), 2) AS average_rating
FROM movies m
JOIN ratings r ON m.movie_id = r.movie_id
WHERE m.release_year IS NOT NULL
GROUP BY m.release_year
ORDER BY m.release_year;