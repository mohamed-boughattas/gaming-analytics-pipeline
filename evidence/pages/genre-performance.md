---
title: Genre Performance
---

```genres_overview
select
    name,
    slug,
    total_games,
    round(avg_rating, 2) as avg_rating,
    total_ratings,
    round(avg_playtime, 1) as avg_playtime
from gaming_analytics.genres
where name is not null
order by total_games desc
```

```genre_games_chart
select
    name,
    total_games,
    avg_rating
from gaming_analytics.genres
where name is not null
order by total_games desc
limit 15
```

```genre_stats
select
    count(*) as total_genres,
    sum(total_games) as total_games_all,
    round(avg(avg_rating), 2) as overall_avg_rating,
    sum(total_ratings) as total_ratings
from gaming_analytics.genres
```

## Genre Performance

<BigValue data={genre_stats} value=total_genres title="Total Genres" />

<BigValue data={genre_stats} value=total_games_all title="Total Games" />

<BigValue data={genre_stats} value=overall_avg_rating title="Overall Avg Rating" />

<BigValue data={genre_stats} value=total_ratings title="Total Ratings" />

### Top Genres by Total Games

<BarChart
    data={genre_games_chart}
    x=name
    y=total_games
    title="Top Genres by Game Count"
    xAxisTitle="Genre"
    yAxisTitle="Total Games"
    swapXY=true
/>

### All Genres

<DataTable data={genres_overview} rows=20>
    <Column id=name title="Genre" />
    <Column id=total_games title="Total Games" />
    <Column id=avg_rating title="Avg Rating" />
    <Column id=total_ratings title="Total Ratings" />
    <Column id=avg_playtime title="Avg Playtime (hrs)" />
</DataTable>
