import numpy as np
import pandas as pd

REGION_COLS = {"NA": "na_sales", "EU": "eu_sales", "JP": "jp_sales"}


def top_platforms_by_region(
    df: pd.DataFrame, top_n: int = 5
) -> dict[str, pd.Series]:
    """Top-N platforms by sales for each region."""
    result = {}
    for region, col in REGION_COLS.items():
        result[region] = df.groupby("platform")[col].sum().sort_values(ascending=False).head(top_n)
    return result


def top_genres_by_region(
    df: pd.DataFrame, top_n: int = 5
) -> dict[str, pd.Series]:
    """Top-N genres by sales for each region."""
    result = {}
    for region, col in REGION_COLS.items():
        result[region] = df.groupby("genre")[col].sum().sort_values(ascending=False).head(top_n)
    return result


def market_share_platforms(df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """Market share (%) of top platforms per region."""
    all_platforms: set[str] = set()
    shares: dict[str, pd.Series] = {}

    for region, col in REGION_COLS.items():
        total = df[col].sum()
        pf_sales = df.groupby("platform")[col].sum().sort_values(ascending=False)
        s = (pf_sales / total * 100).head(top_n)
        shares[region] = s
        all_platforms.update(s.index)

    out = pd.DataFrame(index=sorted(all_platforms))
    for region, s in shares.items():
        out[region] = s
    return out.fillna(0).sort_values("NA", ascending=False)


def market_share_genres(df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """Market share (%) of top genres per region."""
    all_genres: set[str] = set()
    shares: dict[str, pd.Series] = {}

    for region, col in REGION_COLS.items():
        total = df[col].sum()
        genre_sales = df.groupby("genre")[col].sum().sort_values(ascending=False)
        s = (genre_sales / total * 100).head(top_n)
        shares[region] = s
        all_genres.update(s.index)

    out = pd.DataFrame(index=sorted(all_genres))
    for region, s in shares.items():
        out[region] = s
    return out.fillna(0).sort_values("NA", ascending=False)


def rating_sales_by_region(df: pd.DataFrame) -> pd.DataFrame:
    """Total and average sales by rating for each region."""
    all_ratings: set[str] = set()
    total_data: dict[str, pd.Series] = {}
    avg_data: dict[str, pd.Series] = {}

    for region, col in REGION_COLS.items():
        total_data[region] = df.groupby("rating")[col].sum()
        avg_data[region] = df.groupby("rating")[col].mean()
        all_ratings.update(total_data[region].index)

    out = pd.DataFrame(index=sorted(all_ratings))
    for region in REGION_COLS:
        out[f"{region}_total"] = total_data[region]
        out[f"{region}_avg"] = avg_data[region]
    return out.fillna(0)
