import marimo

__generated_with = "0.20.3"
app = marimo.App(width="full")


@app.cell
def _():
    # Connect to DuckDB database
    import duckdb
    import pandas as pd
    import plotly.express as px

    con = duckdb.connect("/app/data/gaming_analytics.duckdb")
    return duckdb, con, pd, px


@app.cell
def _(con, duckdb):
    # Load games data
    games_df = con.execute("""
    show all tables
    """).df()
    return (games_df,)


@app.cell
def _(con, duckdb):
    # Load genres data
    genres_df = con.execute("""
        SELECT
            genre_id,
            name as genre_name,
            games_count,
            updated_at
        FROM mart_genres
        ORDER BY games_count DESC
    """).df()
    return (genres_df,)


@app.cell
def _(con, duckdb):
    # Load platforms data
    platforms_df = con.execute("""
        SELECT
            platform_id,
            name as platform_name,
            games_count,
            updated_at
        FROM mart_platforms
        ORDER BY games_count DESC
    """).df()
    return (platforms_df,)


@app.cell
def _(games_df, marimo):
    # Create games table
    marimo.table(games_df, selection=None)
    return


@app.cell
def _(genres_df, marimo):
    # Create genres table
    marimo.table(genres_df, selection=None)
    return


@app.cell
def _(marimo, platforms_df):
    # Create platforms table
    marimo.table(platforms_df, selection=None)
    return


@app.cell
def _(games_df, marimo, px):
    # Games by rating visualization
    fig = px.scatter(
        games_df.head(50),
        x="rating",
        y="ratings_count",
        size="metacritic",
        color="rating_top",
        hover_name="name",
        title="Games by Rating vs Ratings Count",
        labels={"rating": "Average Rating", "ratings_count": "Number of Ratings"},
    )
    fig.update_layout(height=500)
    marimo.plotly(fig)
    return


@app.cell
def _(genres_df, marimo, px):
    # Top genres by games count
    fig = px.bar(
        genres_df.head(10),
        x="genre_name",
        y="games_count",
        title="Top 10 Genres by Games Count",
        labels={"genre_name": "Genre", "games_count": "Number of Games"},
    )
    fig.update_layout(height=400)
    marimo.plotly(fig)
    return


@app.cell
def _(marimo, platforms_df, px):
    # Top platforms by games count
    fig = px.bar(
        platforms_df.head(10),
        x="platform_name",
        y="games_count",
        title="Top 10 Platforms by Games Count",
        labels={"platform_name": "Platform", "games_count": "Number of Games"},
    )
    fig.update_layout(height=400)
    marimo.plotly(fig)
    return


@app.cell
def _(games_df, marimo, px):
    # Rating distribution
    fig = px.histogram(
        games_df,
        x="rating",
        nbins=20,
        title="Distribution of Game Ratings",
        labels={"rating": "Rating", "count": "Number of Games"},
    )
    fig.update_layout(height=400)
    marimo.plotly(fig)
    return


@app.cell
def _(games_df, marimo, px):
    # Metacritic vs Rating correlation
    fig = px.scatter(
        games_df,
        x="metacritic",
        y="rating",
        trendline="ols",
        title="Metacritic Score vs User Rating Correlation",
        labels={"metacritic": "Metacritic Score", "rating": "User Rating"},
    )
    fig.update_layout(height=500)
    marimo.plotly(fig)
    return


@app.cell
def _(games_df, genres_df, marimo, pd, platforms_df):
    # Data summary statistics
    summary_stats = {
        "Total Games": len(games_df),
        "Average Rating": f"{games_df['rating'].mean():.2f}",
        "Average Metacritic": f"{games_df['metacritic'].mean():.1f}",
        "Total Genres": len(genres_df),
        "Total Platforms": len(platforms_df),
        "Data Last Updated": games_df["updated_at"].max().strftime("%Y-%m-%d %H:%M:%S"),
    }

    summary_df = pd.DataFrame(list(summary_stats.items()), columns=["Metric", "Value"])
    marimo.table(summary_df, selection=None)
    return


if __name__ == "__main__":
    app.run()
