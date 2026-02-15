# Project Games — Video Game Sales Analysis

## 1. Context

The video game industry generates billions of dollars annually across a fragmented landscape of platforms, genres, and regional markets. Publishers, developers, and online stores need data-driven insights to decide where to invest — which platforms to prioritize, which genres to fund, and how to tailor strategies for different geographic markets. However, publicly available sales datasets often suffer from significant missing data (over 50% of critic and user scores are absent), making reliable analysis difficult without a robust data-preparation strategy.

This project uses a historical dataset of **16,715 video game titles** with global and regional sales figures, critic/user scores, ESRB ratings, and metadata spanning from the 1980s to 2016. The data was sourced from aggregated public records of game sales across North America, Europe, Japan, and other markets.

## 2. Problem

The raw dataset presents several challenges that prevent straightforward analysis:

- **Massive missing values:** critic_score (51.3% null), user_score (54.5% null), and rating (40.4% null) are incomplete for more than half the records, making direct comparisons unreliable.
- **Inconsistent data types:** year_of_release stored as floats, user_score encoded as strings, and missing years for games that can be recovered from their titles or cross-platform entries.
- **No clear relevant period:** The dataset spans 38 years, but many early years have very few records, and older platform/genre dynamics no longer reflect the current market.
- **Unanswered business questions:** Which platforms are leading or declining? Which genres deliver the highest return per title? Do user preferences (scores) vary across platforms or genres? How do regional markets (NA, EU, JP) differ in platform and genre preferences?

## 3. Proposed Solution

The project implements an end-to-end analysis pipeline composed of three stages:

**Stage 1 — Data Cleaning and Imputation**
- Standardize column names and data types; recover missing release years from game titles and cross-platform lookups; drop records missing critical fields (name, genre, year); remove duplicates keeping the highest-selling entry.
- Fill missing scores and ratings using a **5-level hierarchical imputation strategy** (game name > platform+genre+year > genre+year > genre > global median/mode), requiring a minimum of 5 samples per group to ensure statistical reliability. This achieved 100% fill rate for critic_score and user_score, and 74% for rating (remaining values marked as "TBD").

**Stage 2 — Exploratory and Statistical Analysis**
- **Temporal analysis:** Identify significant years (above-average releases) and select 2014–2016 as the relevant analysis period.
- **Platform analysis:** Rank platforms by total sales, compute lifecycle metrics, and classify growth trends (GROWTH / STABLE / DECLINE).
- **Genre analysis:** Calculate total and per-game revenue by genre, classifying genres into high-sales and low-sales tiers using quartile thresholds.
- **Regional analysis:** Compare top platforms and genres across NA, EU, and JP; compute market share percentages; analyze ESRB rating impact by region.
- **Hypothesis testing:** Run Welch's t-tests (alpha = 0.05) to evaluate whether user score differences between Xbox One vs PC and Action vs Sports genres are statistically significant.

**Stage 3 — Visualization and Dashboard**
- Static plots (matplotlib/seaborn) and interactive visualizations (Plotly) for every analysis dimension.
- A Streamlit dashboard with six tabs (Overview, Temporal, Platforms, Genres, Regional, Hypothesis Tests) enabling interactive exploration with configurable parameters.

## 4. Key Indicators

| Indicator | Value |
|-----------|-------|
| Total records (raw) | 16,715 |
| Total records (processed) | 16,575 |
| Relevant period | 2014–2016 (1,689 games) |
| Imputation success — critic_score | 100% |
| Imputation success — user_score | 100% |
| Imputation success — rating | 74.1% |
| Top platform (global sales) | PS4 — $288.1M |
| Top genre (total sales) | Action — $199.4M |
| Most profitable genre (sales/game) | Shooter |
| High-sales genre tier | Shooter, Sports, Platform |
| Low-sales genre tier | Adventure, Strategy, Puzzle |
| NA top platform / genre | PS4 ($98.6M) / Shooter ($79.0M) |
| EU top platform / genre | PS4 ($130.0M) / Action ($74.7M) |
| JP top platform / genre | 3DS ($44.2M) / Role-Playing ($31.2M) |
| H1: Xbox One vs PC (user_score) | p = 0.096 — Fail to reject H0 |
| H2: Action vs Sports (user_score) | p < 0.001 — Reject H0 |

---

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
