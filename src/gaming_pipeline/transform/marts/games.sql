MODEL (
    name gaming_analytics.marts_games,
    kind INCREMENTAL,
    start_date '2020-01-01',
    grain id
);

-- Games mart table with enriched metrics
WITH raw_games AS (
    SELECT
        id,
        name,
        slug,
        released,
        tba,
        updated,
        rating,
        rating_top,
        ratings_count,
        reviews_text_count,
        added,
        metacritic,
        playtime,
        screenshots_count,
        movies_count,
        creators_count,
        achievements_count,
        parent_achievements_count,
        reddit_count,
        twitch_count,
        youtube_count,
        suggestions_count,
        rating_1_pct,
        rating_2_pct,
        rating_3_pct,
        rating_4_pct,
        rating_5_pct,
        genre_id,
        platform_id,
        store_id,
        developer_id,
        publisher_id
    FROM gaming_analytics.rawg_games
    WHERE id IS NOT NULL
),

enriched_games AS (
    SELECT
        *,
        -- Calculate rating categories
        CASE
            WHEN rating >= 9 THEN 'Excellent'
            WHEN rating >= 7 THEN 'Good'
            WHEN rating >= 5 THEN 'Average'
            WHEN rating >= 3 THEN 'Below Average'
            ELSE 'Poor'
        END AS rating_category,
        -- Calculate release year and month
        YEAR(released) AS release_year,
        MONTH(released) AS release_month,
        -- Calculate engagement score
        (rating * 0.4 + metacritic / 10 * 0.3 + ratings_count / 100 * 0.3) AS engagement_score
    FROM raw_games
)

SELECT * FROM enriched_games