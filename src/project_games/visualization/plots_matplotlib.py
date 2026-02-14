import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def plot_null_heatmaps(
    df: pd.DataFrame,
    attributes: list[str] | None = None,
    figsize: tuple[int, int] = (24, 14),
) -> plt.Figure:
    """Heatmaps of null-percentage by genre, platform, and year."""
    if attributes is None:
        attributes = ["critic_score", "user_score", "rating"]

    pivot_genre = df.groupby("genre")[attributes].apply(
        lambda x: (x.isna().sum() / len(x)) * 100
    ).sort_index()
    pivot_platform = df.groupby("platform")[attributes].apply(
        lambda x: (x.isna().sum() / len(x)) * 100
    ).sort_index()
    pivot_year = df.groupby("year_of_release")[attributes].apply(
        lambda x: (x.isna().sum() / len(x)) * 100
    ).sort_index()

    fig, axes = plt.subplots(1, 3, figsize=figsize)
    for ax, pivot, title in zip(
        axes,
        [pivot_genre, pivot_platform, pivot_year],
        ["Genre", "Platform", "Year"],
    ):
        sns.heatmap(
            pivot, annot=True, fmt=".1f", cmap="RdYlGn_r", ax=ax,
            cbar_kws={"label": "% Nulls"}, linewidths=0.5, vmin=0, vmax=100,
        )
        ax.set_title(f"Null % by {title}", fontweight="bold")
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=8)
    fig.tight_layout()
    return fig


def plot_games_per_year(games_per_year: pd.Series, figsize: tuple[int, int] = (15, 8)) -> plt.Figure:
    """Line chart of games released per year."""
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(games_per_year.index, games_per_year.values, marker="o", linewidth=2, markersize=5)
    ax.fill_between(games_per_year.index, 0, games_per_year.values, alpha=0.3)
    ax.set_xlabel("Year", fontweight="bold")
    ax.set_ylabel("Games Released", fontweight="bold")
    ax.set_title("Video Game Releases per Year", fontweight="bold")
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def plot_platform_evolution(
    platform_year_sales: pd.DataFrame,
    top_platforms: list[str] | None = None,
    figsize: tuple[int, int] = (16, 12),
) -> plt.Figure:
    """Line chart + heatmap of platform sales over time."""
    if top_platforms is None:
        top_platforms = platform_year_sales.sum(axis=1).nlargest(10).index.tolist()

    fig, axes = plt.subplots(2, 1, figsize=figsize)

    for platform in top_platforms:
        if platform in platform_year_sales.index:
            data = platform_year_sales.loc[platform]
            axes[0].plot(data.index, data.values, marker="o", label=platform, linewidth=2, markersize=4)
    axes[0].set_xlabel("Year", fontweight="bold")
    axes[0].set_ylabel("Total Sales ($M)", fontweight="bold")
    axes[0].set_title("Sales Evolution by Platform", fontweight="bold")
    axes[0].legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=9)
    axes[0].grid(True, alpha=0.3)
    axes[0].xaxis.set_major_locator(plt.MaxNLocator(integer=True))

    recent = platform_year_sales.loc[
        platform_year_sales.index.isin(top_platforms),
        platform_year_sales.columns >= 2000,
    ]
    sns.heatmap(recent, cmap="YlOrRd", annot=False, cbar_kws={"label": "Sales ($M)"}, ax=axes[1])
    axes[1].set_title("Sales Heatmap (2000+)", fontweight="bold")
    fig.tight_layout()
    return fig


def plot_boxplot_by_group(
    df: pd.DataFrame,
    group_col: str,
    value_col: str = "total_sales",
    groups: list[str] | None = None,
    figsize: tuple[int, int] = (16, 7),
) -> plt.Figure:
    """Box plot of *value_col* across categories in *group_col*."""
    if groups is None:
        groups = df[group_col].value_counts().head(10).index.tolist()

    fig, ax = plt.subplots(figsize=figsize)
    box_data = [df[df[group_col] == g][value_col].values for g in groups]
    bp = ax.boxplot(box_data, labels=groups, patch_artist=True, showmeans=True, meanline=True)
    for patch in bp["boxes"]:
        patch.set_facecolor("lightblue")
        patch.set_alpha(0.7)
    ax.set_xlabel(group_col.title(), fontweight="bold")
    ax.set_ylabel(value_col.replace("_", " ").title(), fontweight="bold")
    ax.set_title(f"Distribution of {value_col} by {group_col}", fontweight="bold")
    ax.grid(True, alpha=0.3, axis="y")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return fig


def plot_regional_bars(
    data_by_region: dict[str, pd.Series],
    title: str = "Top by Region",
    figsize: tuple[int, int] = (12, 16),
) -> plt.Figure:
    """Horizontal bar charts for each region (NA/EU/JP)."""
    regions = list(data_by_region.keys())
    fig, axes = plt.subplots(len(regions), 1, figsize=figsize)
    if len(regions) == 1:
        axes = [axes]

    for ax, region in zip(axes, regions):
        series = data_by_region[region]
        colors = plt.cm.Spectral(np.linspace(0, 1, len(series)))
        ax.barh(range(len(series)), series.values, color=colors, edgecolor="black", alpha=0.7)
        ax.set_yticks(range(len(series)))
        ax.set_yticklabels(series.index)
        ax.set_xlabel("Sales ($M)", fontweight="bold")
        ax.set_title(f"{title} - {region}", fontweight="bold")
        ax.invert_yaxis()
        ax.grid(True, alpha=0.3, axis="x")

    fig.tight_layout()
    return fig


def plot_hypothesis_result(
    scores_a: pd.Series,
    scores_b: pd.Series,
    label_a: str,
    label_b: str,
    figsize: tuple[int, int] = (12, 5),
) -> plt.Figure:
    """Histogram + boxplot comparing two score distributions."""
    fig, axes = plt.subplots(1, 2, figsize=figsize)

    axes[0].hist(scores_a, bins=20, alpha=0.7, label=label_a, edgecolor="black")
    axes[0].hist(scores_b, bins=20, alpha=0.7, label=label_b, edgecolor="black")
    axes[0].set_xlabel("Score")
    axes[0].set_ylabel("Frequency")
    axes[0].set_title(f"Distribution: {label_a} vs {label_b}")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].boxplot([scores_a, scores_b], labels=[label_a, label_b])
    axes[1].set_ylabel("Score")
    axes[1].set_title(f"Boxplot: {label_a} vs {label_b}")
    axes[1].grid(True, alpha=0.3)

    fig.tight_layout()
    return fig
