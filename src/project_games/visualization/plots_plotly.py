import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def fig_games_per_year(games_per_year: pd.Series) -> go.Figure:
    """Interactive area chart of games released per year."""
    fig = px.area(
        x=games_per_year.index,
        y=games_per_year.values,
        labels={"x": "Year", "y": "Games Released"},
        title="Video Game Releases per Year",
    )
    fig.update_traces(line=dict(width=2), marker=dict(size=5))
    fig.update_layout(xaxis=dict(dtick=2))
    return fig


def fig_platform_sales(platform_sales: pd.Series, top_n: int = 15) -> go.Figure:
    """Horizontal bar chart of total sales by platform."""
    top = platform_sales.head(top_n)
    fig = px.bar(
        x=top.values,
        y=top.index,
        orientation="h",
        labels={"x": "Total Sales ($M)", "y": "Platform"},
        title=f"Top {top_n} Platforms by Total Sales",
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    return fig


def fig_platform_evolution(
    platform_year_sales: pd.DataFrame,
    top_platforms: list[str] | None = None,
) -> go.Figure:
    """Line chart of platform sales over time."""
    if top_platforms is None:
        top_platforms = platform_year_sales.sum(axis=1).nlargest(10).index.tolist()

    fig = go.Figure()
    for platform in top_platforms:
        if platform in platform_year_sales.index:
            data = platform_year_sales.loc[platform]
            fig.add_trace(go.Scatter(
                x=data.index, y=data.values, mode="lines+markers", name=platform,
            ))
    fig.update_layout(
        title="Sales Evolution by Platform",
        xaxis_title="Year",
        yaxis_title="Total Sales ($M)",
        hovermode="x unified",
    )
    return fig


def fig_platform_heatmap(platform_year_sales: pd.DataFrame, min_year: int = 2000) -> go.Figure:
    """Heatmap of platform sales by year."""
    recent = platform_year_sales.loc[:, platform_year_sales.columns >= min_year]
    fig = px.imshow(
        recent,
        labels=dict(x="Year", y="Platform", color="Sales ($M)"),
        title="Platform Sales Heatmap",
        color_continuous_scale="YlOrRd",
        aspect="auto",
    )
    return fig


def fig_genre_sales(genre_stats: pd.DataFrame) -> go.Figure:
    """Bar chart of total sales and average per game by genre."""
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Total Sales by Genre", "Average Sales per Game"),
    )
    sorted_total = genre_stats.sort_values("sum", ascending=False)
    fig.add_trace(
        go.Bar(x=sorted_total.index, y=sorted_total["sum"], name="Total Sales"),
        row=1, col=1,
    )
    sorted_avg = genre_stats.sort_values("avg_per_game", ascending=False)
    fig.add_trace(
        go.Bar(x=sorted_avg.index, y=sorted_avg["avg_per_game"], name="Avg/Game",
               marker_color="coral"),
        row=1, col=2,
    )
    fig.update_layout(title_text="Genre Analysis", showlegend=False)
    return fig


def fig_boxplot_by_group(
    df: pd.DataFrame,
    group_col: str,
    value_col: str = "total_sales",
    groups: list[str] | None = None,
) -> go.Figure:
    """Interactive box plot of value_col by group_col."""
    subset = df.copy()
    if groups is not None:
        subset = subset[subset[group_col].isin(groups)]
    fig = px.box(
        subset, x=group_col, y=value_col,
        title=f"Distribution of {value_col.replace('_', ' ').title()} by {group_col.title()}",
    )
    return fig


def fig_regional_comparison(
    data_by_region: dict[str, pd.Series],
    title: str = "Regional Comparison",
) -> go.Figure:
    """Grouped bar chart comparing top items across regions."""
    all_items: set[str] = set()
    for s in data_by_region.values():
        all_items.update(s.index)
    items = sorted(all_items)

    fig = go.Figure()
    colors = {"NA": "#1f77b4", "EU": "#ff7f0e", "JP": "#2ca02c"}
    for region, series in data_by_region.items():
        values = [series.get(item, 0) for item in items]
        fig.add_trace(go.Bar(
            name=region, x=items, y=values, marker_color=colors.get(region, None),
        ))
    fig.update_layout(barmode="group", title=title, yaxis_title="Sales ($M)")
    return fig


def fig_market_share_heatmap(share_df: pd.DataFrame, title: str = "Market Share (%)") -> go.Figure:
    """Heatmap of market share by region."""
    fig = px.imshow(
        share_df.T,
        labels=dict(x="Item", y="Region", color="Share (%)"),
        title=title,
        color_continuous_scale="RdYlGn",
        aspect="auto",
        text_auto=".1f",
    )
    return fig


def fig_hypothesis_comparison(
    scores_a: pd.Series,
    scores_b: pd.Series,
    label_a: str,
    label_b: str,
) -> go.Figure:
    """Overlaid histograms + box plots for hypothesis test visualization."""
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(f"Distribution: {label_a} vs {label_b}", "Box Plot"),
    )
    fig.add_trace(
        go.Histogram(x=scores_a, name=label_a, opacity=0.7, nbinsx=25),
        row=1, col=1,
    )
    fig.add_trace(
        go.Histogram(x=scores_b, name=label_b, opacity=0.7, nbinsx=25),
        row=1, col=1,
    )
    fig.add_trace(
        go.Box(y=scores_a, name=label_a), row=1, col=2,
    )
    fig.add_trace(
        go.Box(y=scores_b, name=label_b), row=1, col=2,
    )
    fig.update_layout(barmode="overlay", title_text="Hypothesis Test Visualization")
    return fig


def fig_rating_by_region(rating_df: pd.DataFrame) -> go.Figure:
    """Grouped bars of rating sales by region."""
    total_cols = [c for c in rating_df.columns if c.endswith("_total")]
    regions = [c.replace("_total", "") for c in total_cols]

    fig = go.Figure()
    for col, region in zip(total_cols, regions):
        fig.add_trace(go.Bar(
            name=region, x=rating_df.index, y=rating_df[col],
        ))
    fig.update_layout(
        barmode="group",
        title="Sales by ESRB Rating and Region",
        xaxis_title="Rating",
        yaxis_title="Total Sales ($M)",
    )
    return fig
