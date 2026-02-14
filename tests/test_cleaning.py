import numpy as np
import pandas as pd
import pytest

from project_games.data.cleaning import (
    add_total_sales,
    cast_types,
    clean_dataset,
    drop_duplicates,
    drop_incomplete_rows,
    fill_year_of_release,
    standardize_columns,
)


@pytest.fixture
def raw_df():
    return pd.DataFrame(
        {
            "Name": ["Game A", "Game B", "FIFA 2014", None, "Game E"],
            "Platform": ["PS4", "PC", "XOne", "PS4", "PC"],
            "Year_of_Release": [2015.0, np.nan, np.nan, 2014.0, 2016.0],
            "Genre": ["Action", "Sports", "Sports", None, "Action"],
            "NA_Sales": [1.0, 2.0, 0.5, 0.1, 3.0],
            "EU_Sales": [0.5, 1.0, 0.2, 0.0, 1.5],
            "JP_Sales": [0.1, 0.0, 0.0, 0.0, 0.2],
            "Other_Sales": [0.1, 0.2, 0.1, 0.0, 0.3],
            "Critic_Score": [85.0, np.nan, 70.0, np.nan, 90.0],
            "User_Score": ["8.5", "tbd", "7.0", np.nan, "9.0"],
            "Rating": ["M", np.nan, "E", np.nan, "T"],
        }
    )


def test_standardize_columns(raw_df):
    result = standardize_columns(raw_df)
    assert all(c == c.lower() for c in result.columns)
    assert "name" in result.columns


def test_cast_types(raw_df):
    df = standardize_columns(raw_df)
    result = cast_types(df)
    assert result["year_of_release"].dtype.name == "Int64"
    assert result["user_score"].dtype == float
    assert pd.isna(result.loc[1, "user_score"])


def test_fill_year_from_name(raw_df):
    df = standardize_columns(raw_df)
    df = cast_types(df)
    result = fill_year_of_release(df)
    val = result.loc[2, "year_of_release"]
    assert pd.notna(val) and int(val) == 2014


def test_drop_incomplete_rows(raw_df):
    df = standardize_columns(raw_df)
    df = cast_types(df)
    df = fill_year_of_release(df)
    result = drop_incomplete_rows(df)
    assert result["name"].isna().sum() == 0
    assert result["genre"].isna().sum() == 0


def test_add_total_sales(raw_df):
    df = standardize_columns(raw_df)
    result = add_total_sales(df)
    assert "total_sales" in result.columns
    assert result.loc[0, "total_sales"] == pytest.approx(1.7)


def test_drop_duplicates():
    df = pd.DataFrame(
        {
            "name": ["A", "A", "B"],
            "platform": ["PS4", "PS4", "PC"],
            "genre": ["Action", "Action", "RPG"],
            "year_of_release": [2015, 2015, 2016],
            "total_sales": [1.0, 2.0, 3.0],
        }
    )
    result = drop_duplicates(df)
    assert len(result) == 2
    kept = result[result["name"] == "A"]
    assert kept.iloc[0]["total_sales"] == 2.0


def test_clean_dataset_end_to_end(raw_df):
    result = clean_dataset(raw_df)
    assert "total_sales" in result.columns
    assert result["name"].isna().sum() == 0
    assert result["genre"].isna().sum() == 0
    assert all(c == c.lower() for c in result.columns)
