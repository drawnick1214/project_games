import pandas as pd


def genre_distribution(df: pd.DataFrame) -> pd.Series:
    """Count of games per genre, sorted descending."""
    return df["genre"].value_counts()


def genre_sales_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sales statistics by genre."""
    stats = (
        df.groupby("genre")["total_sales"]
        .agg(["sum", "mean", "median", "count"])
        .sort_values("sum", ascending=False)
    )
    stats["avg_per_game"] = stats["sum"] / stats["count"]
    return stats


def classify_genres(df: pd.DataFrame) -> dict[str, list[str]]:
    """Classify genres into high/low sales tiers using quartiles."""
    stats = genre_sales_summary(df)
    q75 = stats["avg_per_game"].quantile(0.75)
    q25 = stats["avg_per_game"].quantile(0.25)
    return {
        "high_sales": stats[stats["avg_per_game"] >= q75].index.tolist(),
        "low_sales": stats[stats["avg_per_game"] <= q25].index.tolist(),
    }
