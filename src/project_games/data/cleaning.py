import numpy as np
import pandas as pd


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Lowercase all column names."""
    df = df.copy()
    df.columns = [c.lower() for c in df.columns]
    return df


def cast_types(df: pd.DataFrame) -> pd.DataFrame:
    """Fix dtypes for year_of_release and user_score."""
    df = df.copy()
    df["year_of_release"] = pd.to_numeric(df["year_of_release"], errors="coerce").astype("Int64")
    df["user_score"] = pd.to_numeric(df["user_score"], errors="coerce").astype("float")
    return df


def _assign_year_from_name(row: pd.Series) -> int | None:
    """Try to extract a 4-digit year from the game name."""
    if pd.isna(row["name"]):
        return None
    for word in str(row["name"]).split():
        if word.isdigit() and len(word) == 4:
            return int(word)
        if word.isdigit() and len(word) == 2:
            return int("20" + word) if int(word) < 20 else int("19" + word)
    return None


def fill_year_of_release(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing year_of_release using name heuristics and cross-platform lookup."""
    df = df.copy()

    # 1. Extract year from game name
    mask = df["year_of_release"].isna() | (df["year_of_release"] == 0)
    df.loc[mask, "year_of_release"] = df.loc[mask].apply(_assign_year_from_name, axis=1)

    # 2. Fill from same game on another platform
    year_by_game = (
        df.groupby("name")["year_of_release"]
        .apply(lambda x: x.dropna().mode().iloc[0] if not x.dropna().empty else np.nan)
        .to_dict()
    )
    mask_nan = df["year_of_release"].isna()
    df.loc[mask_nan, "year_of_release"] = df.loc[mask_nan, "name"].map(year_by_game)

    return df


def drop_incomplete_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows missing name, genre, or year_of_release."""
    df = df.copy()
    df.dropna(subset=["name"], inplace=True)
    df.dropna(subset=["genre"], inplace=True)
    df.dropna(subset=["year_of_release"], inplace=True)
    return df


def add_total_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Add total_sales column as sum of regional sales."""
    df = df.copy()
    df["total_sales"] = df["na_sales"] + df["eu_sales"] + df["jp_sales"] + df["other_sales"]
    return df


def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate games keeping the entry with highest total_sales."""
    df = df.copy()
    if "total_sales" not in df.columns:
        df = add_total_sales(df)
    df = (
        df.sort_values("total_sales", ascending=False)
        .drop_duplicates(subset=["name", "platform", "genre", "year_of_release"], keep="first")
    )
    return df


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Run the full cleaning pipeline (no imputation)."""
    df = standardize_columns(df)
    df = cast_types(df)
    df = fill_year_of_release(df)
    df = drop_incomplete_rows(df)
    df = add_total_sales(df)
    df = drop_duplicates(df)
    return df.reset_index(drop=True)
