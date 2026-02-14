import numpy as np
import pandas as pd

from project_games.config import load_config


def _agg_func(column: str, df: pd.DataFrame):
    """Return the appropriate aggregation callable (mode for categorical, median for numeric)."""
    is_categorical = df[column].dtype == "object" or column == "rating"
    if is_categorical:
        return lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else np.nan
    return "median"


def impute_hierarchical(
    df: pd.DataFrame,
    column: str,
    min_samples: int = 5,
    max_level: int = 4,
) -> tuple[pd.Series, pd.Series]:
    """Impute missing values using a hierarchical grouping strategy.

    Levels:
        0. Match by game name
        1. platform + genre + year_of_release
        2. genre + year_of_release
        3. genre
        4. Global (median or mode)

    Returns:
        (imputed_values, imputation_levels)
    """
    imputed_col = df[column].copy()
    imputation_level = pd.Series("original", index=df.index)
    imputation_level[df[column].isna()] = "not_imputed"

    is_categorical = df[column].dtype == "object" or column == "rating"
    agg_func = _agg_func(column, df)

    hierarchies = {
        0: ["name"],
        1: ["platform", "genre", "year_of_release"],
        2: ["genre", "year_of_release"],
        3: ["genre"],
        4: None,  # global
    }

    for level in range(max_level + 1):
        mask = imputed_col.isna()
        if not mask.any():
            break

        group_cols = hierarchies[level]

        if group_cols is None:
            # Global level
            if is_categorical:
                mode = df[column].mode()
                global_value = mode.iloc[0] if len(mode) > 0 else np.nan
            else:
                global_value = df[column].median()

            if pd.notna(global_value):
                imputed_col[mask] = global_value
                imputation_level[mask] = f"level_{level}"
        else:
            if not all(col in df.columns for col in group_cols):
                continue

            level_stats = df.groupby(group_cols)[column].agg(value=agg_func, count="count")
            level_stats = level_stats[level_stats["count"] >= min_samples]

            for idx in df[mask].index:
                group_key = (
                    tuple(df.loc[idx, col] for col in group_cols)
                    if len(group_cols) > 1
                    else df.loc[idx, group_cols[0]]
                )
                if group_key in level_stats.index:
                    value = level_stats.loc[group_key, "value"]
                    if pd.notna(value):
                        imputed_col.at[idx] = value
                        imputation_level.at[idx] = f"level_{level}"

    # Mark remaining nulls as TBD for categorical columns
    remaining = imputed_col.isna()
    if remaining.any() and is_categorical:
        imputed_col[remaining] = "TBD"
        imputation_level[remaining] = "TBD"

    return imputed_col, imputation_level


def impute_dataset(df: pd.DataFrame, cfg: dict | None = None) -> pd.DataFrame:
    """Run hierarchical imputation on critic_score, user_score, and rating.

    Returns a new DataFrame with imputed values (imputation-level columns are dropped).
    """
    if cfg is None:
        cfg = load_config()

    df = df.copy()

    # critic_score and user_score: all levels (0-4)
    df["critic_score"], _ = impute_hierarchical(df, "critic_score", min_samples=5, max_level=4)
    df["user_score"], _ = impute_hierarchical(df, "user_score", min_samples=5, max_level=4)

    # rating: levels 0-2 only, rest becomes TBD
    df["rating"], _ = impute_hierarchical(df, "rating", min_samples=5, max_level=2)

    return df
