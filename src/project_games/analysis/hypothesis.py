from dataclasses import dataclass

import pandas as pd
from scipy import stats

from project_games.config import load_config


@dataclass
class HypothesisResult:
    name: str
    group_a_label: str
    group_b_label: str
    n_a: int
    n_b: int
    mean_a: float
    mean_b: float
    t_statistic: float
    p_value: float
    alpha: float
    reject_null: bool

    def summary(self) -> str:
        verdict = "REJECT H0" if self.reject_null else "FAIL TO REJECT H0"
        return (
            f"{self.name}: {self.group_a_label} (n={self.n_a}, mean={self.mean_a:.4f}) "
            f"vs {self.group_b_label} (n={self.n_b}, mean={self.mean_b:.4f}) | "
            f"t={self.t_statistic:.4f}, p={self.p_value:.6f} => {verdict}"
        )


def run_ttest(
    df: pd.DataFrame,
    column: str,
    group_column: str,
    group_a: str,
    group_b: str,
    alpha: float = 0.05,
    name: str = "",
) -> HypothesisResult:
    """Run Welch's t-test comparing *column* between two groups."""
    scores_a = df[df[group_column] == group_a][column].dropna()
    scores_b = df[df[group_column] == group_b][column].dropna()

    if len(scores_a) < 2 or len(scores_b) < 2:
        raise ValueError(
            f"Insufficient data: {group_a}={len(scores_a)}, {group_b}={len(scores_b)}"
        )

    t_stat, p_val = stats.ttest_ind(scores_a, scores_b, equal_var=False)

    return HypothesisResult(
        name=name or f"{group_a}_vs_{group_b}",
        group_a_label=group_a,
        group_b_label=group_b,
        n_a=len(scores_a),
        n_b=len(scores_b),
        mean_a=scores_a.mean(),
        mean_b=scores_b.mean(),
        t_statistic=t_stat,
        p_value=p_val,
        alpha=alpha,
        reject_null=p_val < alpha,
    )


def run_configured_tests(
    df: pd.DataFrame, cfg: dict | None = None
) -> list[HypothesisResult]:
    """Run all hypothesis tests defined in config/default.yaml."""
    if cfg is None:
        cfg = load_config()

    alpha = cfg["analysis"]["significance_level"]
    results = []

    for test_cfg in cfg["hypothesis_tests"]:
        result = run_ttest(
            df,
            column=test_cfg["column"],
            group_column=test_cfg["group_column"],
            group_a=test_cfg["group_a"],
            group_b=test_cfg["group_b"],
            alpha=alpha,
            name=test_cfg["name"],
        )
        results.append(result)

    return results
