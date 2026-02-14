#!/usr/bin/env python3
"""Run the full analysis pipeline on processed data."""

from project_games.analysis.genre import classify_genres, genre_sales_summary
from project_games.analysis.hypothesis import run_configured_tests
from project_games.analysis.platform import (
    platform_growth_analysis,
    platform_total_sales,
    platform_yearly_sales,
)
from project_games.analysis.regional import (
    market_share_genres,
    market_share_platforms,
    rating_sales_by_region,
    top_genres_by_region,
    top_platforms_by_region,
)
from project_games.analysis.temporal import (
    filter_relevant_period,
    games_per_year,
    significant_years,
)
from project_games.config import load_config
from project_games.data.loader import load_processed_data


def main() -> None:
    cfg = load_config()

    print("Loading processed data...")
    df = load_processed_data()
    print(f"  {len(df)} rows loaded")

    # --- Temporal analysis ---
    print("\n--- Temporal Analysis ---")
    gpy = games_per_year(df)
    sig = significant_years(df)
    print(f"  Years with data: {len(gpy)}")
    print(f"  Significant years (>= mean): {len(sig)} ({sig.index.min()}-{sig.index.max()})")

    # --- Filter to relevant period ---
    df_rel = filter_relevant_period(df, cfg)
    start = cfg["analysis"]["relevant_period"]["start_year"]
    print(f"\n  Relevant period ({start}+): {len(df_rel)} rows")

    # --- Platform analysis ---
    print("\n--- Platform Analysis ---")
    ps = platform_total_sales(df_rel)
    print(f"  Top 5 platforms: {', '.join(ps.head(5).index)}")

    growth = platform_growth_analysis(df_rel)
    for _, row in growth.head(5).iterrows():
        print(f"    {row['platform']}: ${row['total_sales']:.1f}M, trend={row['trend']}")

    # --- Genre analysis ---
    print("\n--- Genre Analysis ---")
    gs = genre_sales_summary(df_rel)
    print(f"  Top 5 genres by total sales:")
    for genre in gs.head(5).index:
        print(f"    {genre}: ${gs.loc[genre, 'sum']:.1f}M ({gs.loc[genre, 'count']:.0f} games)")

    tiers = classify_genres(df_rel)
    print(f"  High-sales genres: {', '.join(tiers['high_sales'])}")
    print(f"  Low-sales genres: {', '.join(tiers['low_sales'])}")

    # --- Regional analysis ---
    print("\n--- Regional Analysis ---")
    for region, series in top_platforms_by_region(df_rel).items():
        print(f"  {region} top platform: {series.index[0]} (${series.iloc[0]:.1f}M)")
    for region, series in top_genres_by_region(df_rel).items():
        print(f"  {region} top genre: {series.index[0]} (${series.iloc[0]:.1f}M)")

    # --- Hypothesis tests ---
    print("\n--- Hypothesis Tests ---")
    results = run_configured_tests(df_rel, cfg)
    for r in results:
        print(f"  {r.summary()}")

    print("\nAnalysis complete.")


if __name__ == "__main__":
    main()
