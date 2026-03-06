---
title: Gaming Analytics Dashboard
page_type: dashboard
priority: 1
---

# 🎮 Gaming Analytics

Welcome to the Gaming Analytics dashboard. This dashboard provides insights into video game data from the RAWG API.

## 📊 Key Metrics

```sql games_kpi
SELECT
    COUNT(*) AS total_games,
    AVG(rating) AS avg_rating,
    AVG(metacritic) AS avg_metacritic,
    SUM(playtime) AS total_playtime_hours
FROM gaming_analytics.marts_games
```

## 📈 Top Rated Games

```sql top_games
SELECT
    name,
    rating,
    metacritic,
    release_year
FROM gaming_analytics.marts_games
WHERE rating >= 9.0
ORDER BY rating DESC, metacritic DESC
LIMIT 10
```

## 🏷️ Genre Distribution

```sql genre_dist
SELECT
    UNNEST(genre_names) AS genre,
    COUNT(*) AS game_count
FROM gaming_analytics.marts_games
GROUP BY genre
ORDER BY game_count DESC
LIMIT 10
```

---

*Built with [Evidence](https://evidence.dev/) - SQL-native analytics dashboard*
