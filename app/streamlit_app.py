"""Interactive Video Game Sales Dashboard — Streamlit app."""

import streamlit as st
import pandas as pd

from project_games.config import load_config
from project_games.data.loader import load_processed_data
from project_games.analysis.temporal import games_per_year, filter_relevant_period
from project_games.analysis.platform import (
    platform_total_sales,
    platform_yearly_sales,
    platform_growth_analysis,
    platform_lifecycle,
)
from project_games.analysis.genre import genre_sales_summary, classify_genres
from project_games.analysis.regional import (
    top_platforms_by_region,
    top_genres_by_region,
    market_share_platforms,
    market_share_genres,
    rating_sales_by_region,
)
from project_games.analysis.hypothesis import run_configured_tests
from project_games.visualization.plots_plotly import (
    fig_games_per_year,
    fig_platform_sales,
    fig_platform_evolution,
    fig_platform_heatmap,
    fig_genre_sales,
    fig_boxplot_by_group,
    fig_regional_comparison,
    fig_market_share_heatmap,
    fig_hypothesis_comparison,
    fig_rating_by_region,
)

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Video Game Sales Dashboard",
    page_icon="🎮",
    layout="wide",
)


@st.cache_data
def load_data():
    cfg = load_config()
    df = load_processed_data()
    df_rel = filter_relevant_period(df, cfg)
    return df, df_rel, cfg


df_full, df_rel, cfg = load_data()

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
st.sidebar.title("🎮 Video Game Sales")
st.sidebar.markdown("---")

tab_choice = st.sidebar.radio(
    "Section",
    ["Overview", "Temporal", "Platforms", "Genres", "Regional", "Hypothesis Tests"],
)

start_year = cfg["analysis"]["relevant_period"]["start_year"]
st.sidebar.markdown("---")
st.sidebar.caption(f"Relevant period: {start_year}–2016")
st.sidebar.caption(f"Total records: {len(df_full):,}")
st.sidebar.caption(f"Filtered records: {len(df_rel):,}")

# ---------------------------------------------------------------------------
# Overview
# ---------------------------------------------------------------------------
if tab_choice == "Overview":
    st.title("Video Game Sales — Overview")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Games", f"{len(df_rel):,}")
    c2.metric("Platforms", df_rel["platform"].nunique())
    c3.metric("Genres", df_rel["genre"].nunique())
    c4.metric("Total Sales", f"${df_rel['total_sales'].sum():,.1f}M")

    st.markdown("---")
    st.subheader("Dataset sample")
    st.dataframe(df_rel.head(20), use_container_width=True)

# ---------------------------------------------------------------------------
# Temporal
# ---------------------------------------------------------------------------
elif tab_choice == "Temporal":
    st.title("Temporal Analysis")

    gpy = games_per_year(df_full)
    st.plotly_chart(fig_games_per_year(gpy), use_container_width=True)

    st.markdown("### Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Peak Year", f"{int(gpy.idxmax())} ({gpy.max()} games)")
    col2.metric("Mean / Year", f"{gpy.mean():.0f}")
    col3.metric("Years with Data", len(gpy))

# ---------------------------------------------------------------------------
# Platforms
# ---------------------------------------------------------------------------
elif tab_choice == "Platforms":
    st.title("Platform Analysis")

    ps = platform_total_sales(df_rel)
    top_n = st.slider("Top N platforms", 5, 20, 10)
    top_list = ps.head(top_n).index.tolist()

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Sales Ranking", "Evolution", "Heatmap", "Growth & Lifecycle"]
    )

    with tab1:
        st.plotly_chart(fig_platform_sales(ps, top_n), use_container_width=True)

    with tab2:
        pys = platform_yearly_sales(df_rel, top_list)
        st.plotly_chart(fig_platform_evolution(pys, top_list), use_container_width=True)

    with tab3:
        pys_all = platform_yearly_sales(df_rel, top_list)
        st.plotly_chart(fig_platform_heatmap(pys_all, min_year=start_year), use_container_width=True)

    with tab4:
        st.subheader("Growth Analysis")
        growth = platform_growth_analysis(df_rel)
        st.dataframe(growth, use_container_width=True)

        st.subheader("Lifecycle")
        pys_lc = platform_yearly_sales(df_rel, top_list)
        lc = platform_lifecycle(pys_lc)
        st.dataframe(lc, use_container_width=True)

    st.markdown("---")
    st.subheader("Sales Distribution")
    st.plotly_chart(
        fig_boxplot_by_group(df_rel, "platform", groups=top_list),
        use_container_width=True,
    )

# ---------------------------------------------------------------------------
# Genres
# ---------------------------------------------------------------------------
elif tab_choice == "Genres":
    st.title("Genre Analysis")

    gs = genre_sales_summary(df_rel)
    st.plotly_chart(fig_genre_sales(gs), use_container_width=True)

    tiers = classify_genres(df_rel)
    col1, col2 = st.columns(2)
    col1.success(f"**High-sales genres:** {', '.join(tiers['high_sales'])}")
    col2.warning(f"**Low-sales genres:** {', '.join(tiers['low_sales'])}")

    st.markdown("---")
    st.subheader("Sales Distribution by Genre")
    top_genres = gs.head(8).index.tolist()
    st.plotly_chart(
        fig_boxplot_by_group(df_rel, "genre", groups=top_genres),
        use_container_width=True,
    )

    st.subheader("Full Stats")
    st.dataframe(gs, use_container_width=True)

# ---------------------------------------------------------------------------
# Regional
# ---------------------------------------------------------------------------
elif tab_choice == "Regional":
    st.title("Regional Analysis")

    region_tab = st.radio(
        "Focus", ["Platforms by Region", "Genres by Region", "Ratings by Region"],
        horizontal=True,
    )

    if region_tab == "Platforms by Region":
        data = top_platforms_by_region(df_rel)
        st.plotly_chart(
            fig_regional_comparison(data, "Top 5 Platforms by Region"),
            use_container_width=True,
        )
        share = market_share_platforms(df_rel)
        st.plotly_chart(
            fig_market_share_heatmap(share, "Platform Market Share (%)"),
            use_container_width=True,
        )

    elif region_tab == "Genres by Region":
        data = top_genres_by_region(df_rel)
        st.plotly_chart(
            fig_regional_comparison(data, "Top 5 Genres by Region"),
            use_container_width=True,
        )
        share = market_share_genres(df_rel)
        st.plotly_chart(
            fig_market_share_heatmap(share, "Genre Market Share (%)"),
            use_container_width=True,
        )

    else:
        rating_df = rating_sales_by_region(df_rel)
        st.plotly_chart(fig_rating_by_region(rating_df), use_container_width=True)
        st.dataframe(rating_df, use_container_width=True)

# ---------------------------------------------------------------------------
# Hypothesis Tests
# ---------------------------------------------------------------------------
elif tab_choice == "Hypothesis Tests":
    st.title("Hypothesis Tests")
    st.markdown(f"**Significance level (α):** {cfg['analysis']['significance_level']}")

    results = run_configured_tests(df_rel, cfg)

    for r in results:
        with st.expander(f"{'✅' if r.reject_null else '❌'} {r.name}: {r.group_a_label} vs {r.group_b_label}", expanded=True):
            c1, c2, c3 = st.columns(3)
            c1.metric(f"{r.group_a_label} mean", f"{r.mean_a:.4f}", f"n={r.n_a}")
            c2.metric(f"{r.group_b_label} mean", f"{r.mean_b:.4f}", f"n={r.n_b}")
            c3.metric("p-value", f"{r.p_value:.6f}")

            verdict = "**REJECT H₀** — Statistically significant difference" if r.reject_null else "**FAIL TO REJECT H₀** — No significant difference found"
            st.markdown(verdict)

            scores_a = df_rel[df_rel[cfg["hypothesis_tests"][results.index(r)]["group_column"]] == r.group_a_label][cfg["hypothesis_tests"][results.index(r)]["column"]].dropna()
            scores_b = df_rel[df_rel[cfg["hypothesis_tests"][results.index(r)]["group_column"]] == r.group_b_label][cfg["hypothesis_tests"][results.index(r)]["column"]].dropna()

            st.plotly_chart(
                fig_hypothesis_comparison(scores_a, scores_b, r.group_a_label, r.group_b_label),
                use_container_width=True,
            )
