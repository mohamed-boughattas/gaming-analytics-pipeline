---
title: Gaming Analytics Dashboard
---

# Gaming Analytics Dashboard

Welcome to the Gaming Analytics dashboard powered by Evidence, DuckDB, and SQLMesh.

## Key Metrics

```sql games_overview
SELECT
  total_games,
  avg_rating,
  avg_metacritic,
  total_playtime_hours,
  avg_engagement_score
FROM games_overview
```

<BigValue
  data={games_overview}
  value=total_games
  title="Total Games"
/>

<BigValue
  data={games_overview}
  value=avg_rating
  title="Avg Rating"
  fmt="#.00"
/>

<BigValue
  data={games_overview}
  value=avg_engagement_score
  title="Avg Engagement Score"
  fmt="#.00"
/>

<BigValue
  data={games_overview}
  value=total_playtime_hours
  title="Total Playtime (hrs)"
  fmt="#,##0"
/>

## Top Rated Games

```sql top_games
SELECT
  name,
  rating,
  metacritic,
  release_year,
  rating_category,
  engagement_score,
  genre_count,
  platform_count
FROM top_games
```

<DataTable data={top_games} />

## Rating Distribution

```sql rating_dist
SELECT
  rating_category,
  game_count
FROM rating_dist
```

<BarChart
  data={rating_dist}
  x=rating_category
  y=game_count
  title="Games by Rating Category"
/>

## Engagement vs Rating

```sql engagement_scatter
SELECT
  name,
  rating,
  engagement_score,
  rating_category,
  release_year
FROM engagement_scatter
```

<ScatterPlot
  data={engagement_scatter}
  x=rating
  y=engagement_score
  title="Engagement Score vs Rating"
  color=rating_category
/>

## Genre Analytics

```sql genre_analytics
SELECT
  genre_name,
  total_games,
  avg_rating,
  avg_metacritic,
  excellent_pct
FROM genre_analytics
```

<DataTable data={genre_analytics} />

<BarChart
  data={genre_analytics}
  x=genre_name
  y=excellent_pct
  title="% Excellent Games by Genre"
/>

## Games by Release Year

```sql games_by_year
SELECT
  release_year,
  game_count,
  avg_rating,
  avg_engagement
FROM games_by_year
```

<LineChart
  data={games_by_year}
  x=release_year
  y=game_count
  title="Games by Release Year"
/>

---

_Built with [Evidence](https://evidence.dev) - SQL-native analytics powered by SQLMesh_
