# Project Games — Video Game Sales Analysis

## Executive Summary

This project delivers an end-to-end analysis of global video game sales across platforms, genres, and regions, drawing from a dataset of **16,715 game titles**. After cleaning and hierarchical imputation of missing values, the processed dataset retains **16,575 records** spanning 38 years of release history (1980s–2016). The analysis focuses on the **2014–2016 relevant period** (1,689 games) to derive actionable, up-to-date market insights.

### Key Findings

**Platform Landscape (2014–2016)**

| Platform | Total Sales | Rank |
|----------|------------|------|
| PS4      | $288.1M    | 1    |
| Xbox One | $140.4M    | 2    |
| 3DS      | $86.7M     | 3    |
| PS3      | $68.2M     | 4    |
| X360     | $48.2M     | 5    |

PS4 dominates global sales with more than double the revenue of its nearest competitor (Xbox One). The previous generation (PS3/X360) continues to contribute meaningful sales even during this period.

**Genre Performance**

- **Top revenue genres:** Action ($199.4M, 619 games), Shooter ($170.9M, 128 games), Sports ($109.5M, 161 games), Role-Playing ($101.4M, 221 games).
- **Highest revenue-per-game tiers:** Shooter, Sports, and Platform genres rank highest in average sales per title.
- **Lower-performing genres:** Adventure, Strategy, and Puzzle fall in the bottom quartile of per-game revenue.

Shooters generate the highest revenue per title despite having far fewer releases than Action, indicating strong per-title commercial performance.

**Regional Market Differences**

| Region | Top Platform | Top Genre |
|--------|-------------|-----------|
| North America | PS4 ($98.6M) | Shooter ($79.0M) |
| Europe | PS4 ($130.0M) | Action ($74.7M) |
| Japan | 3DS ($44.2M) | Role-Playing ($31.2M) |

The Japanese market stands apart with a clear preference for handheld platforms (3DS) and RPGs, while Western markets (NA/EU) favor home consoles and action/shooter titles. PS4 leads in both NA and EU, with Europe representing its strongest regional market.

**Statistical Hypothesis Tests (alpha = 0.05)**

1. **Xbox One vs PC user scores:** No statistically significant difference was found (t = 1.67, p = 0.096). Users rate games similarly on both platforms.
2. **Action vs Sports user scores:** A highly significant difference was detected (t = 12.32, p < 0.001). Action games receive substantially higher user ratings (mean 6.94) than Sports titles (mean 5.21).

### Methodology

- **Data cleaning:** Column standardization, type casting, year recovery from game names, cross-platform year lookup, deduplication by highest-selling entry.
- **Imputation:** A 5-level hierarchical strategy fills missing critic scores, user scores, and ratings — from exact game-name matches down to global medians/modes, requiring a minimum of 5 samples per group.
- **Statistical testing:** Welch's two-sample t-test (unequal variances) at the 0.05 significance level.

---

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
make install
```

## Usage

### Preprocess raw data

```bash
make preprocess
```

Loads `data/raw/games.csv`, cleans columns, imputes missing values, and writes `data/processed/games_complete.csv`.

### Run analysis

```bash
make analyze
```

Runs temporal, platform, genre, regional, and hypothesis-testing analyses on the processed data.

### Run tests

```bash
make test
```

### Launch interactive dashboard

```bash
pip install -e ".[app]"
make app
```

Opens a Streamlit dashboard with tabs for Overview, Temporal, Platforms, Genres, Regional, and Hypothesis Tests.

## Project Structure

```
config/default.yaml          Configuration (paths, params)
src/project_games/           Python package
  data/                      Loading, cleaning, imputation
  analysis/                  Temporal, platform, genre, regional, hypothesis
  visualization/             Matplotlib and Plotly plotting helpers
app/                         Streamlit dashboard
scripts/                     CLI entry points
notebooks/                   EDA notebooks
tests/                       Unit tests
```

## Tech Stack

- **Data processing:** pandas, numpy, scipy
- **Visualization:** matplotlib, seaborn, plotly
- **Dashboard:** Streamlit
- **Testing:** pytest
- **Linting:** ruff
