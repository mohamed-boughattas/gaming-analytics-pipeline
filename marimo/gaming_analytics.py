import marimo

__generated_with = "0.15.1"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo

    mo.md("# Gaming Analytics Dashboard")
    return (mo,)


@app.cell
def _():
    # Connect to DuckDB database
    import duckdb
    import pandas as pd
    import plotly.express as px

    from gaming_pipeline.config import settings

    con = duckdb.connect(settings.database.path, read_only=True)
    return con, pd, px


@app.cell
def _(con, mo):
    # Load games data
    games_df = con.execute(
        """
        SELECT *
        FROM marts.games
        ORDER BY released DESC
        LIMIT 1000
    """
    ).df()
    mo.ui.table(games_df)
    return (games_df,)


@app.cell
def _(con, mo):
    # Load genres data
    genres_df = con.execute(
        """
        SELECT
            id as genre_id,
            name,
            total_games as games_count,
            avg_rating,
            excellent_pct,
            good_pct
        FROM marts.genres
        ORDER BY total_games DESC
    """
    ).df()
    mo.ui.table(genres_df)
    return (genres_df,)


@app.cell
def _(con, mo):
    # Load platforms data
    platforms_df = con.execute(
        """
        SELECT
            id as platform_id,
            name as platform_name,
            total_games as games_count,
            avg_rating,
            year_start
        FROM marts.platforms
        ORDER BY total_games DESC
    """
    ).df()
    mo.ui.table(platforms_df)
    return (platforms_df,)


@app.cell
def _(games_df, mo):
    # KPI Summary Cards
    total_games = len(games_df)
    avg_rating = games_df["rating"].mean()
    avg_metacritic = games_df["metacritic"].mean()

    kpi_row = mo.hstack(
        [
            mo.stat(label="Total Games", value=f"{total_games:,}"),
            mo.stat(label="Avg Rating", value=f"{avg_rating:.2f}"),
            mo.stat(label="Avg Metacritic", value=f"{avg_metacritic:.1f}"),
        ],
        gap=2,
    )
    kpi_row  # noqa: B018
    return


@app.cell
def _(games_df, mo):
    # Interactive filters
    year_slider = mo.ui.slider(
        games_df["release_year"].min(),
        games_df["release_year"].max(),
        value=games_df["release_year"].max(),
        label="Filter by Year",
    )

    min_rating = mo.ui.number(value=0, start=0, stop=10, step=0.1, label="Min Rating")

    mo.md(f"**Filters:** {year_slider} | {min_rating}")
    return min_rating, year_slider


@app.cell
def _(games_df, min_rating, mo, px, year_slider):
    # Filtered data based on user input
    filtered_games = games_df[
        (games_df["release_year"] <= year_slider.value)
        & (games_df["rating"] >= min_rating.value)
    ]

    # Games by rating visualization
    fig = px.scatter(
        filtered_games.head(100),
        x="rating",
        y="ratings_count",
        size="metacritic",
        color="rating_category",
        hover_name="name",
        title="Games by Rating vs Ratings Count (Filtered)",
        labels={"rating": "Average Rating", "ratings_count": "Number of Ratings"},
    )
    fig.update_layout(height=500)
    mo.ui.plotly(fig)
    return (filtered_games,)


@app.cell
def _(filtered_games, mo, px):
    # Rating distribution by category
    rating_category_fig = px.histogram(
        filtered_games,
        x="rating_category",
        title="Games by Rating Category",
        labels={"rating_category": "Rating Category", "count": "Number of Games"},
    )
    rating_category_fig.update_layout(height=400)
    mo.ui.plotly(rating_category_fig)
    return


@app.cell
def _(genres_df, mo, px):
    # Top genres by games count
    genres_fig = px.bar(
        genres_df.head(10),
        x="name",
        y="games_count",
        color="avg_rating",
        title="Top 10 Genres by Games Count",
        labels={"name": "Genre", "games_count": "Number of Games"},
        color_continuous_scale="Viridis",
    )
    genres_fig.update_layout(height=400)
    mo.ui.plotly(genres_fig)
    return


@app.cell
def _(mo, platforms_df, px):
    # Platforms by games count
    platforms_fig = px.bar(
        platforms_df.head(15),
        x="platform_name",
        y="games_count",
        color="avg_rating",
        title="Top Platforms by Games Count",
        labels={"platform_name": "Platform", "games_count": "Number of Games"},
        color_continuous_scale="Viridis",
    )
    platforms_fig.update_layout(height=400)
    mo.ui.plotly(platforms_fig)
    return


@app.cell
def _(games_df, mo, px):
    # Rating distribution histogram
    rating_dist_fig = px.histogram(
        games_df,
        x="rating",
        nbins=20,
        title="Distribution of Game Ratings",
        labels={"rating": "Rating", "count": "Number of Games"},
    )
    rating_dist_fig.update_layout(height=400)
    mo.ui.plotly(rating_dist_fig)
    return


@app.cell
def _(games_df, mo, px):
    # Metacritic vs Rating correlation
    metacritic_fig = px.scatter(
        games_df,
        x="metacritic",
        y="rating",
        color="rating_category",
        title="Metacritic Score vs User Rating Correlation",
        labels={"metacritic": "Metacritic Score", "rating": "User Rating"},
    )
    metacritic_fig.update_layout(height=500)
    mo.ui.plotly(metacritic_fig)
    return


@app.cell
def _(games_df, mo, px):
    # Games released over time (yearly trend)
    yearly_games = games_df.groupby("release_year").size().reset_index(name="count")
    yearly_fig = px.line(
        yearly_games,
        x="release_year",
        y="count",
        title="Games Released by Year",
        labels={"release_year": "Year", "count": "Number of Games"},
    )
    yearly_fig.update_layout(height=400)
    mo.ui.plotly(yearly_fig)
    return


@app.cell
def _(games_df, genres_df, mo, pd, platforms_df):
    # Data summary statistics
    summary_stats = {
        "Total Games": len(games_df),
        "Average Rating": f"{games_df['rating'].mean():.2f}",
        "Average Metacritic": f"{games_df['metacritic'].mean():.1f}",
        "Total Genres": len(genres_df),
        "Total Platforms": len(platforms_df),
        "Data Last Updated": games_df["updated"].max().strftime("%Y-%m-%d %H:%M:%S"),
    }

    summary_df = pd.DataFrame(list(summary_stats.items()), columns=["Metric", "Value"])
    mo.ui.table(summary_df)
    return


@app.cell
def _(games_df, mo):
    # Show raw table with all columns
    mo.md("### Games Table (Raw Data)")
    mo.ui.table(games_df)
    return


@app.cell
def _(genres_df, mo):
    # Show genres table
    mo.md("### Genres Table")
    mo.ui.table(genres_df)
    return


@app.cell
def _(mo, platforms_df):
    # Show platforms table
    mo.md("### Platforms Table")
    mo.ui.table(platforms_df)
    return


if __name__ == "__main__":
    app.run()
