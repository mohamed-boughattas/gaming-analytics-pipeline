MODEL (
    name gaming_analytics.marts_genres,
    kind FULL,
    grain id
);

-- Genres mart table with aggregated metrics
WITH genres AS (
    SELECT
        id,
        name,
        slug,
        games_count,
        image_background
    FROM gaming_analytics.rawg_genres
    WHERE id IS NOT NULL
),

genre_metrics AS (
    SELECT
        g.id,
        g.name,
        g.slug,
        g.image_background,
        -- Aggregate game metrics by genre
        COUNT(DISTINCT ga.id) AS total_games,
        AVG(ga.rating) AS avg_rating,
        AVG(ga.metacritic) AS avg_metacritic,
        MAX(ga.rating) AS max_rating,
        MIN(ga.rating) AS min_rating,
        SUM(ga.ratings_count) AS total_ratings,
        AVG(ga.ratings_count) AS avg_ratings_per_game,
        -- Count games by rating category
        SUM(CASE WHEN ga.rating >= 9 THEN 1 ELSE 0 END) AS excellent_games,
        SUM(CASE WHEN ga.rating >= 7 AND ga.rating < 9 THEN 1 ELSE 0 END) AS good_games,
        SUM(CASE WHEN ga.rating >= 5 AND ga.rating < 7 THEN 1 ELSE 0 END) AS average_games,
        SUM(CASE WHEN ga.rating < 5 THEN 1 ELSE 0 END) AS below_average_games
    FROM genres g
    LEFT JOIN gaming_analytics.rawg_games ga ON g.id = ga.genre_id
    GROUP BY g.id, g.name, g.slug, g.image_background
)

SELECT * FROM genre_metrics