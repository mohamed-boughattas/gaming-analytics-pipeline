---
title: Release Trends
---

```releases_by_year
select
    release_year as year,
    count(*) as game_count,
    round(avg(rating), 2) as avg_rating,
    sum(ratings_count) as total_ratings
from gaming_analytics.games
where release_year is not null
group by release_year
order by release_year
```

```quarterly_current
select
    case
        when release_month between 1 and 3 then 'Q1'
        when release_month between 4 and 6 then 'Q2'
        when release_month between 7 and 9 then 'Q3'
        else 'Q4'
    end as quarter,
    count(*) as release_count
from gaming_analytics.games
where release_year = (select max(release_year) from gaming_analytics.games where release_year is not null)
group by quarter
order by case quarter
    when 'Q1' then 1
    when 'Q2' then 2
    when 'Q3' then 3
    when 'Q4' then 4
end
```

```top_release_years
select
    release_year as year,
    count(*) as game_count
from gaming_analytics.games
where release_year is not null
group by release_year
order by game_count desc
limit 10
```

## Release Trends

### Releases Over Time

<LineChart
    data={releases_by_year}
    x=year
    y=game_count
    title="Games Released by Year"
    xAxisTitle="Year"
    yAxisTitle="Number of Games"
/>

### Average Rating by Release Year

<LineChart
    data={releases_by_year}
    x=year
    y=avg_rating
    title="Average Game Rating by Year"
    xAxisTitle="Year"
    yAxisTitle="Avg Rating"
/>

### Quarterly Releases (Latest Year)

<BarChart
    data={quarterly_current}
    x=quarter
    y=release_count
    title="Releases by Quarter (Latest Year)"
    xAxisTitle="Quarter"
    yAxisTitle="Releases"
/>

### Busiest Release Years

<DataTable data={top_release_years} rows=10>
    <Column id=year title="Year" />
    <Column id=game_count title="Games Released" />
</DataTable>
