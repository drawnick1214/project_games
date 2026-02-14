#!/usr/bin/env python3
"""Load raw data, clean it, impute missing values, and save to processed/."""

from project_games.config import get_project_root, load_config
from project_games.data.cleaning import clean_dataset
from project_games.data.imputation import impute_dataset
from project_games.data.loader import load_raw_data


def main() -> None:
    cfg = load_config()
    root = get_project_root()

    print("Loading raw data...")
    df = load_raw_data()
    print(f"  Loaded {len(df)} rows")

    print("Cleaning...")
    df = clean_dataset(df)
    print(f"  After cleaning: {len(df)} rows")

    print("Imputing missing values...")
    df = impute_dataset(df, cfg)
    print(f"  After imputation: {len(df)} rows")

    out_path = root / cfg["data"]["processed_path"]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Saved to {out_path}")


if __name__ == "__main__":
    main()
