# Project Games - Video Game Sales Analysis

Analysis pipeline for video game sales data: preprocessing, hierarchical imputation, exploratory analysis, and hypothesis testing.

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

### Launch dashboard (Phase 2)

```bash
pip install -e ".[app]"
make app
```

## Project Structure

```
config/default.yaml          Configuration (paths, params)
src/project_games/           Python package
  data/                      Loading, cleaning, imputation
  analysis/                  Temporal, platform, genre, regional, hypothesis
  visualization/             Matplotlib and Plotly plotting helpers
scripts/                     CLI entry points
app/                         Streamlit dashboard
notebooks/                   EDA notebooks
tests/                       Unit tests
```
