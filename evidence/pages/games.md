---
title: Games Analytics
page_type: page
priority: 2
---

# Games Analytics

Detailed analysis of game data across ratings, release dates, and platforms.

## Rating Distribution

```sql rating_distribution
SELECT
    rating_category,
    COUNT(*) AS game_count
FROM gaming_analytics.marts_games
GROUP BY rating_category
ORDER BY
    CASE rating_category
        WHEN 'Excellent' THEN 1
        WHEN 'Good' THEN 2
        WHEN 'Average' THEN 3
        WHEN 'Below Average' THEN 4
        ELSE 5
    END
```

## Games by Release Year

```sql games_by_year
SELECT
    release_year,
    COUNT(*) AS game_count,
    AVG(rating) AS avg_rating
FROM gaming_analytics.marts_games
WHERE release_year IS NOT NULL
GROUP BY release_year
ORDER BY release_year DESC
LIMIT 15
```

## Most Played Games

```sql most_played
SELECT
    name,
    playtime,
    rating,
    release_year
FROM gaming_analytics.marts_games
WHERE playtime > 0
ORDER BY playtime DESC
LIMIT 10
```

## Platform Availability

```sql platform_counts
SELECT
    UNNEST(platform_names) AS platform,
    COUNT(DISTINCT id) AS game_count
FROM gaming_analytics.marts_games
GROUP BY platform
ORDER BY game_count DESC
```

---

*See [Overview](/) for summary metrics*
