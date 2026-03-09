import marimo

__generated_with = "0.20.4"
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

    con = duckdb.connect(settings.database.path)
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
def _(games_df, mo, px):
    def _():
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
        return mo.ui.plotly(fig)

    _()
    return


@app.cell
def _(genres_df, mo, px):
    def _():
        # Top genres by games count
        fig = px.bar(
            genres_df.head(10),
            x="name",
            y="games_count",
            title="Top 10 Genres by Games Count",
            labels={"name": "Genre", "games_count": "Number of Games"},
        )
        fig.update_layout(height=400)
        return mo.ui.plotly(fig)

    _()
    return


@app.cell
def _(mo, platforms_df, px):
    def _():
        def _():
            # Top platforms by games count
            fig = px.bar(
                platforms_df.head(10),
                x="platform_name",
                y="games_count",
                title="Top 10 Platforms by Games Count",
                labels={"platform_name": "Platform", "games_count": "Number of Games"},
            )
            fig.update_layout(height=400)
            return mo.ui.plotly(fig)

        return _()

    _()
    return


@app.cell
def _(games_df, mo, px):
    def _():
        # Rating distribution
        fig = px.histogram(
            games_df,
            x="rating",
            nbins=20,
            title="Distribution of Game Ratings",
            labels={"rating": "Rating", "count": "Number of Games"},
        )
        fig.update_layout(height=400)
        return mo.ui.plotly(fig)

    _()
    return


@app.cell
def _(games_df, mo, px):
    def _():
        # Metacritic vs Rating correlation
        fig = px.scatter(
            games_df,
            x="metacritic",
            y="rating",
            title="Metacritic Score vs User Rating Correlation",
            labels={"metacritic": "Metacritic Score", "rating": "User Rating"},
        )
        fig.update_layout(height=500)
        return mo.ui.plotly(fig)

    _()
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


if __name__ == "__main__":
    app.run()
