import numpy as np
import pandas as pd
import pytest

from project_games.data.imputation import impute_hierarchical


@pytest.fixture
def sample_df():
    """Small dataset with known nulls for testing hierarchical imputation."""
    return pd.DataFrame(
        {
            "name": ["A", "A", "B", "B", "C", "C", "D", "D", "E", "E", "F", "F"],
            "platform": ["PS4"] * 6 + ["PC"] * 6,
            "genre": ["Action"] * 4 + ["Sports"] * 4 + ["Action"] * 2 + ["Sports"] * 2,
            "year_of_release": [2015] * 12,
            "critic_score": [80, 85, np.nan, 70, 75, np.nan, 90, 88, np.nan, 60, 65, np.nan],
            "user_score": [8.0, 8.5, np.nan, 7.0, 7.5, np.nan, 9.0, 8.8, np.nan, 6.0, 6.5, np.nan],
            "rating": ["M", "M", np.nan, "E", "T", np.nan, "M", "T", np.nan, "E", "E", np.nan],
        }
    )


def test_impute_numeric_fills_nulls(sample_df):
    imputed, levels = impute_hierarchical(sample_df, "critic_score", min_samples=1, max_level=4)
    assert imputed.isna().sum() == 0
    assert imputed.iloc[0] == 80


def test_impute_categorical_fills_nulls(sample_df):
    imputed, levels = impute_hierarchical(sample_df, "rating", min_samples=1, max_level=4)
    assert imputed.isna().sum() == 0


def test_impute_preserves_originals(sample_df):
    imputed, levels = impute_hierarchical(sample_df, "critic_score", min_samples=1, max_level=4)
    assert imputed.iloc[0] == 80
    assert imputed.iloc[1] == 85
    assert imputed.iloc[3] == 70


def test_impute_levels_tracked(sample_df):
    imputed, levels = impute_hierarchical(sample_df, "critic_score", min_samples=1, max_level=4)
    assert levels.iloc[0] == "original"
    assert levels.iloc[2] != "not_imputed"


def test_impute_with_high_min_samples(sample_df):
    imputed, levels = impute_hierarchical(sample_df, "critic_score", min_samples=100, max_level=4)
    assert imputed.isna().sum() == 0
    assert (levels == "level_4").sum() > 0


def test_impute_user_score(sample_df):
    imputed, levels = impute_hierarchical(sample_df, "user_score", min_samples=1, max_level=4)
    assert imputed.isna().sum() == 0
    assert imputed.iloc[0] == 8.0


def test_impute_rating_max_level_2(sample_df):
    imputed, levels = impute_hierarchical(sample_df, "rating", min_samples=1, max_level=2)
    assert imputed.isna().sum() == 0
