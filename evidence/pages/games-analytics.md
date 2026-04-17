---
title: Games Analytics
---

```games_by_year
select
    release_year as year,
    count(*) as game_count,
    round(avg(rating), 2) as avg_rating,
    sum(reviews_count) as total_reviews
from gaming_analytics.games
where release_year is not null
group by release_year
order by release_year desc
```

```rating_vs_playtime
select
    name,
    rating,
    playtime,
    reviews_count,
    engagement_score
from gaming_analytics.games
where rating is not null and playtime is not null
order by rating desc
limit 100
```

```rating_category_breakdown
select
    rating_category,
    count(*) as count,
    round(avg(rating), 2) as avg_rating,
    sum(reviews_count) as total_reviews
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

## Games Analytics

### Games by Release Year

<LineChart
    data={games_by_year}
    x=year
    y=game_count
    title="Game Releases Over Time"
    xAxisTitle="Year"
    yAxisTitle="Number of Games"
/>

### Rating vs Playtime

<ScatterPlot
    data={rating_vs_playtime}
    x=playtime
    y=rating
    size=reviews_count
    title="Rating vs Playtime (size = reviews)"
    xAxisTitle="Playtime (hrs)"
    yAxisTitle="Rating"
/>

### Rating Category Breakdown

<DataTable data={rating_category_breakdown} rows=10>
    <Column id=rating_category title="Rating Category" />
    <Column id=count title="Count" />
    <Column id=avg_rating title="Avg Rating" />
    <Column id=total_reviews title="Total Reviews" />
</DataTable>
