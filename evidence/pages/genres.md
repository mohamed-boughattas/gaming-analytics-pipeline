---
title: Genre Analytics
page_type: page
priority: 3
---

# Genre Analytics

Analysis of game genres and their performance metrics.

## Genre Performance

```sql genre_performance
SELECT
    genre_name,
    COUNT(*) AS game_count,
    AVG(rating) AS avg_rating,
    AVG(metacritic) AS avg_metacritic,
    AVG(engagement_score) AS avg_engagement
FROM (
    SELECT UNNEST(genre_names) AS genre_name, rating, metacritic, engagement_score
    FROM gaming_analytics.marts_games
)
GROUP BY genre_name
ORDER BY avg_rating DESC
```

## Top Genres by Engagement

```sql top_genres_by_engagement
SELECT
    genre_name,
    AVG(engagement_score) AS avg_engagement_score,
    COUNT(*) AS game_count
FROM (
    SELECT UNNEST(genre_names) AS genre_name, engagement_score
    FROM gaming_analytics.marts_games
)
GROUP BY genre_name
ORDER BY avg_engagement_score DESC
LIMIT 10
```

## Genre Rating Distribution

```sql genre_rating_dist
SELECT
    CASE
        WHEN rating >= 9.0 THEN 'Excellent (9+)'
        WHEN rating >= 7.0 THEN 'Good (7-8.9)'
        WHEN rating >= 5.0 THEN 'Average (5-6.9)'
        WHEN rating >= 3.0 THEN 'Below Average (3-4.9)'
        ELSE 'Poor (<3)'
    END AS rating_category,
    COUNT(*) AS game_count
FROM gaming_analytics.marts_games
WHERE genre_names IS NOT NULL
GROUP BY rating_category
ORDER BY
    CASE rating_category
        WHEN 'Excellent (9+)' THEN 1
        WHEN 'Good (7-8.9)' THEN 2
        WHEN 'Average (5-6.9)' THEN 3
        WHEN 'Below Average (3-4.9)' THEN 4
        ELSE 5
    END
```

## Multi-Genre Games

```sql multi_genre_games
SELECT
    genre_count,
    COUNT(*) AS game_count,
    AVG(rating) AS avg_rating
FROM (
    SELECT id, genre_count, rating
    FROM gaming_analytics.marts_games
)
GROUP BY genre_count
ORDER BY genre_count
```

---

*See [Overview](/) for summary metrics*
