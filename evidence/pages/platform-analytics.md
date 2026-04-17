---
title: Platform Analytics
---

```platforms_overview
select
    name,
    slug,
    year_start,
    total_games,
    round(avg_rating, 2) as avg_rating,
    total_ratings,
    round(avg_playtime, 1) as avg_playtime
from gaming_analytics.platforms
where name is not null
order by total_games desc
```

```platform_games_chart
select
    name,
    total_games,
    avg_rating
from gaming_analytics.platforms
where name is not null
order by total_games desc
limit 15
```

```platform_stats
select
    count(*) as total_platforms,
    sum(total_games) as total_games_all,
    round(avg(avg_rating), 2) as overall_avg_rating,
    sum(total_ratings) as total_ratings
from gaming_analytics.platforms
```

## Platform Analytics

<BigValue data={platform_stats} value=total_platforms title="Total Platforms" />

<BigValue data={platform_stats} value=total_games_all title="Total Games" />

<BigValue data={platform_stats} value=overall_avg_rating title="Overall Avg Rating" />

<BigValue data={platform_stats} value=total_ratings title="Total Ratings" />

### Top Platforms by Total Games

<BarChart
    data={platform_games_chart}
    x=name
    y=total_games
    title="Top Platforms by Game Count"
    xAxisTitle="Platform"
    yAxisTitle="Total Games"
    swapXY=true
/>

### All Platforms

<DataTable data={platforms_overview} rows=20>
    <Column id=name title="Platform" />
    <Column id=year_start title="Start Year" />
    <Column id=total_games title="Total Games" />
    <Column id=avg_rating title="Avg Rating" />
    <Column id=total_ratings title="Total Ratings" />
    <Column id=avg_playtime title="Avg Playtime (hrs)" />
</DataTable>
