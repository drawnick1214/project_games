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
    # No nulls should remain
    assert imputed.isna().sum() == 0
    # Original values are preserved
    assert imputed.iloc[0] == 80


def test_impute_categorical_fills_nulls(sample_df):
    imputed, levels = impute_hierarchical(sample_df, "rating", min_samples=1, max_level=4)
    # No nulls should remain (might be TBD for unfilled)
    assert imputed.isna().sum() == 0


def test_impute_preserves_originals(sample_df):
    imputed, levels = impute_hierarchical(sample_df, "critic_score", min_samples=1, max_level=4)
    # Original non-null values unchanged
    assert imputed.iloc[0] == 80
    assert imputed.iloc[1] == 85
    assert imputed.iloc[3] == 70


def test_impute_levels_tracked(sample_df):
    imputed, levels = impute_hierarchical(sample_df, "critic_score", min_samples=1, max_level=4)
    # Non-null originals should be "original"
    assert levels.iloc[0] == "original"
    # Previously-null values should have a level assigned
    assert levels.iloc[2] != "not_imputed"


def test_impute_with_high_min_samples(sample_df):
    """When min_samples is very high, only global level should work."""
    imputed, levels = impute_hierarchical(sample_df, "critic_score", min_samples=100, max_level=4)
    # Global level (4) should handle everything since groups are too small
    null_count = imputed.isna().sum()
    assert null_count == 0
    # Most imputed values should be at level_4 (global)
    level_4_count = (levels == "level_4").sum()
    assert level_4_count > 0


def test_impute_user_score(sample_df):
    imputed, levels = impute_hierarchical(sample_df, "user_score", min_samples=1, max_level=4)
    assert imputed.isna().sum() == 0
    assert imputed.iloc[0] == 8.0


def test_impute_rating_max_level_2(sample_df):
    """Rating with max_level=2 should leave some as TBD if groups are too small."""
    imputed, levels = impute_hierarchical(sample_df, "rating", min_samples=1, max_level=2)
    assert imputed.isna().sum() == 0
    # All should be filled (either imputed or TBD)
    assert (imputed == "").sum() == 0
