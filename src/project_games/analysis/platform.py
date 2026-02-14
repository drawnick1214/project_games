import numpy as np
import pandas as pd


def platform_total_sales(df: pd.DataFrame) -> pd.Series:
    """Total sales per platform, sorted descending."""
    return df.groupby("platform")["total_sales"].sum().sort_values(ascending=False)


def platform_yearly_sales(df: pd.DataFrame, top_platforms: list[str] | None = None) -> pd.DataFrame:
    """Pivot table: platforms (rows) x years (columns) with total_sales values."""
    subset = df.copy()
    if top_platforms is not None:
        subset = subset[subset["platform"].isin(top_platforms)]
    return (
        subset.groupby(["platform", "year_of_release"])["total_sales"]
        .sum()
        .unstack(fill_value=0)
    )


def platform_lifecycle(platform_year_sales: pd.DataFrame) -> pd.DataFrame:
    """Compute lifecycle metrics for each platform."""
    rows = []
    max_year = platform_year_sales.columns.max()

    for platform in platform_year_sales.index:
        sales = platform_year_sales.loc[platform]
        active = sales[sales > 0]
        if len(active) == 0:
            continue

        peak_year = active.idxmax()
        rows.append(
            {
                "platform": platform,
                "first_year": int(active.index.min()),
                "last_year": int(active.index.max()),
                "peak_year": int(peak_year),
                "peak_sales": active.loc[peak_year],
                "life_cycle": int(active.index.max() - active.index.min() + 1),
                "total_sales": sales.sum(),
                "is_active": sales[sales.index >= max_year].sum() > 0,
            }
        )
    return pd.DataFrame(rows).sort_values("total_sales", ascending=False).reset_index(drop=True)


def platform_growth_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Compute growth rates and trends for each platform."""
    sales_by_platform = platform_total_sales(df)
    yearly = platform_yearly_sales(df)

    rows = []
    for platform in sales_by_platform.index:
        if platform not in yearly.index:
            continue
        series = yearly.loc[platform]
        active = series[series > 0]
        if len(active) < 2:
            continue

        first_sales = active.iloc[0]
        last_sales = active.iloc[-1]
        growth_rate = ((last_sales - first_sales) / first_sales * 100) if first_sales > 0 else 0.0

        if len(active) >= 4:
            early_avg = active.iloc[:2].mean()
            recent_avg = active.iloc[-2:].mean()
            trend_pct = ((recent_avg - early_avg) / early_avg * 100) if early_avg > 0 else 0.0
            if trend_pct > 20:
                trend = "GROWTH"
            elif trend_pct < -20:
                trend = "DECLINE"
            else:
                trend = "STABLE"
        else:
            trend = "N/A"

        rows.append(
            {
                "platform": platform,
                "total_sales": sales_by_platform[platform],
                "growth_rate": growth_rate,
                "trend": trend,
                "last_year_sales": last_sales,
            }
        )
    return pd.DataFrame(rows).sort_values("total_sales", ascending=False).reset_index(drop=True)


def platform_sales_stats(df: pd.DataFrame, platforms: list[str] | None = None) -> pd.DataFrame:
    """Descriptive stats of total_sales grouped by platform."""
    subset = df.copy()
    if platforms is not None:
        subset = subset[subset["platform"].isin(platforms)]
    return subset.groupby("platform")["total_sales"].describe()


def score_sales_correlation(
    df: pd.DataFrame, platform: str
) -> dict[str, float]:
    """Pearson correlation between critic/user scores and total_sales for one platform."""
    pf = df[df["platform"] == platform].copy()
    pf["critic_score_norm"] = pf["critic_score"] / 10 if pf["critic_score"].max() > 10 else pf["critic_score"]
    pf["user_score"] = pd.to_numeric(pf["user_score"], errors="coerce")
    clean = pf[["critic_score_norm", "user_score", "total_sales"]].dropna()

    if len(clean) < 10:
        return {"critic_score": np.nan, "user_score": np.nan}

    return {
        "critic_score": clean["critic_score_norm"].corr(clean["total_sales"]),
        "user_score": clean["user_score"].corr(clean["total_sales"]),
    }


def multiplatform_analysis(
    df: pd.DataFrame, min_platforms: int = 4, max_games: int = 20
) -> pd.DataFrame:
    """Analyse games released on multiple platforms."""
    counts = df.groupby("name")["platform"].nunique()
    games = counts[counts >= min_platforms].index.tolist()[:max_games]

    rows = []
    for game in games:
        for _, row in df[df["name"] == game].iterrows():
            rows.append({"game": game, "platform": row["platform"], "sales": row["total_sales"]})

    return pd.DataFrame(rows)
