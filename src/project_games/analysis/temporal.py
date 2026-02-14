import pandas as pd

from project_games.config import load_config


def games_per_year(df: pd.DataFrame) -> pd.Series:
    """Count the number of games released per year."""
    df_year = df[df["year_of_release"].notna()].copy()
    df_year["year_of_release"] = df_year["year_of_release"].astype(int)
    return df_year.groupby("year_of_release").size().sort_index()


def significant_years(df: pd.DataFrame, threshold: float | None = None) -> pd.Series:
    """Return years with at least *threshold* games (defaults to the mean)."""
    counts = games_per_year(df)
    if threshold is None:
        threshold = counts.mean()
    return counts[counts >= threshold]


def evaluate_lookback_windows(
    df: pd.DataFrame,
    current_year: int = 2016,
    lookback_years: list[int] | None = None,
) -> pd.DataFrame:
    """Compare different time-window sizes for model training."""
    if lookback_years is None:
        lookback_years = [3, 4, 5, 6, 7, 8]

    df_year = df[df["year_of_release"].notna()].copy()
    df_year["year_of_release"] = df_year["year_of_release"].astype(int)

    rows = []
    for yb in lookback_years:
        start = current_year - yb + 1
        window = df_year[df_year["year_of_release"] >= start]
        rows.append(
            {
                "period": f"{start}-{current_year}",
                "years": yb,
                "games": len(window),
                "platforms": window["platform"].nunique(),
                "total_sales": window["total_sales"].sum(),
                "avg_games_per_year": len(window) / yb,
            }
        )
    return pd.DataFrame(rows)


def filter_relevant_period(
    df: pd.DataFrame,
    cfg: dict | None = None,
) -> pd.DataFrame:
    """Filter the dataset to the relevant analysis period from config."""
    if cfg is None:
        cfg = load_config()

    start = cfg["analysis"]["relevant_period"]["start_year"]
    df_rel = df[df["year_of_release"].notna()].copy()
    df_rel["year_of_release"] = df_rel["year_of_release"].astype(int)
    return df_rel[df_rel["year_of_release"] >= start].reset_index(drop=True)
