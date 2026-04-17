---
title: Gaming Overview
---

```games_overview
select
    count(*) as total_games,
    round(avg(rating), 2) as avg_rating,
    sum(playtime) as total_playtime,
    sum(reviews_count) as total_reviews
from gaming_analytics.games
```

```rating_distribution
select
    rating_category,
    count(*) as game_count
from gaming_analytics.games
where rating_category is not null
group by rating_category
order by case rating_category
    when 'Excellent' then 1
    when 'Good' then 2
    when 'Average' then 3
    when 'Below Average' then 4
    when 'Poor' then 5
end
```

```top_games
select
    name,
    rating,
    release_year,
    playtime
from gaming_analytics.games
where rating is not null
order by rating desc
limit 10
```

```excellent_games
select
    count(*) as excellent_count
from gaming_analytics.games
where rating >= 4.5
```

```avg_engagement
select
    round(avg(engagement_score), 2) as avg_engagement
from gaming_analytics.games
```

## Gaming Overview

<BigValue data={games_overview} value=total_games title="Total Games" />

<BigValue data={games_overview} value=avg_rating title="Average Rating" />

<BigValue data={games_overview} value=total_playtime title="Total Playtime (hrs)" />

<BigValue data={games_overview} value=total_reviews title="Total Reviews" />

<BigValue data={excellent_games} value=excellent_count title="Excellent Games (rating >= 4.5)" />

<BigValue data={avg_engagement} value=avg_engagement title="Avg Engagement Score" />

### Rating Distribution

<BarChart
    data={rating_distribution}
    x=rating_category
    y=game_count
    title="Games by Rating Category"
    xAxisTitle="Rating Category"
    yAxisTitle="Number of Games"
/>

### Top 10 Rated Games

<DataTable data={top_games} rows=10>
    <Column id=name title="Game" />
    <Column id=rating title="Rating" />
    <Column id=release_year title="Year" />
    <Column id=playtime title="Playtime (hrs)" />
</DataTable>
