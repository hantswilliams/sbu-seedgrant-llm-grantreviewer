#!/usr/bin/env python3
"""
Reproduce every quantitative result reported in:

    Williams H, Lamberg J, Lamberg E (2026). Evaluating large language models as
    grant reviewers: a comparative study of prompt engineering strategies.
    Front. Educ. 11:1856134. doi: 10.3389/feduc.2026.1856134

Inputs (de-identified, in ../data/):
    human_reviews.csv   12 human reviews (3 applications x 4 reviewers)
    llm_reviews.csv     81 LLM reviews (3 experiments x 3 applications x 3 vendors x 3 iterations)

Outputs (in ./output/):
    results.json        all statistics, machine-readable
    tables.md           Table 2, Table 3, criterion-level and recommendation tables

Analysis plan (see Methods 2.5 of the article):
  * LLM iterations are averaged within each vendor x application cell before
    inferential testing (9 cells in Exp 1, 6 cells in Exps 2-3).
  * Independent-samples Student's t-tests compare LLM cell means with
    individual human scores.
  * Glass's delta uses the human SD as the denominator; 95% CIs for the mean
    difference and for Glass's delta are bootstrap intervals (10,000
    resamples, resampling humans and LLM cells independently). Percentile
    intervals are reported in tables.md; bias-corrected intervals are also
    stored in results.json.
  * A linear mixed-effects model per experiment (REML) on the same data that
    enter the t-test (individual human scores + LLM cell means):
    total ~ reviewer_type, with variance components for rater identity
    (human reviewer or LLM vendor) and application.
  * Criterion-level t-tests (same aggregation) with Holm-Bonferroni correction
    across the six criteria within each experiment.
  * Recommendation agreement: each vendor x application cell reduced to its
    modal recommendation across the 3 iterations, then paired with every human
    review of that application (36 pairs in Exp 1, 24 in Exps 2-3). Cohen's
    kappa at the exact (3-category) and broad (Fund/Fund-with-revisions vs Do
    Not Fund) levels. A sensitivity kappa over all raw human-LLM pairs is also
    reported.
  * Exploratory one-way ANOVA across the three prompt conditions restricted to
    the applications common to all experiments (FC1, FC2), n = 6 cells each.
  * Vendor-level descriptive means and deviation from the human mean (Table 3).
  * Within-application score dispersion (SD) for humans vs LLM raw scores.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import cohen_kappa_score
import statsmodels.formula.api as smf

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)

SEED = 20251007          # date of data collection; any seed gives CIs within rounding
N_BOOT = 10_000

EXPERIMENTS = {
    "exp1_zero_shot": {"label": "Exp 1: Zero-shot", "training_app": None},
    "exp2_few_shot": {"label": "Exp 2: Few-shot", "training_app": "FC3"},
    "exp3_few_shot_strict": {"label": "Exp 3: Few-shot + strict", "training_app": "FC3"},
}
CRITERIA = {
    "innovation_impact": "Innovation & Impact",
    "methodological_approach": "Methodology & Feasibility",
    "research_team_strength": "Team Strength",
    "external_funding_potential": "External Funding Potential",
    "budget_clarity": "Budget Clarity",
    "presentation_quality": "Presentation Quality",
}
VENDOR_LABEL = {"Google": "Gemini 2.5 Flash", "OpenAI": "GPT-5 Nano", "xAI": "Grok 4 Fast"}
REC_ORDER = ["Fund", "Fund with Revisions", "Do Not Fund"]


# ----------------------------------------------------------------------------- helpers
def load():
    human = pd.read_csv(DATA / "human_reviews.csv")
    llm = pd.read_csv(DATA / "llm_reviews.csv")
    return human, llm


def subset(human, llm, exp):
    """Human and LLM rows entering the comparison for one experiment."""
    cfg = EXPERIMENTS[exp]
    l = llm[llm["experiment"] == exp].copy()
    h = human.copy()
    if cfg["training_app"]:
        l = l[l["application"] != cfg["training_app"]]
        h = h[h["application"] != cfg["training_app"]]
    return h, l


def cell_means(l, col="total_score"):
    """Average the 3 iterations within each vendor x application cell."""
    return l.groupby(["vendor", "application"], as_index=False)[col].mean()


def bootstrap_ci(stat_fn, h, l, rng, n_boot=N_BOOT, alpha=0.05):
    """Bootstrap CI, resampling humans and LLM cells independently.

    Returns (percentile_low, percentile_high, bc_low, bc_high). The percentile
    interval reproduces the intervals in Table 2 of the article to within
    Monte Carlo error; the bias-corrected (BC) interval is also stored in
    results.json for reference.
    """
    theta = stat_fn(h, l)
    boots = np.empty(n_boot)
    nh, nl = len(h), len(l)
    for i in range(n_boot):
        hb = h[rng.integers(0, nh, nh)]
        lb = l[rng.integers(0, nl, nl)]
        boots[i] = stat_fn(hb, lb)
    boots = boots[np.isfinite(boots)]
    p_lo, p_hi = np.quantile(boots, [alpha / 2, 1 - alpha / 2])
    z0 = stats.norm.ppf(np.clip((boots < theta).mean(), 1e-6, 1 - 1e-6))
    lo = stats.norm.cdf(2 * z0 + stats.norm.ppf(alpha / 2))
    hi = stats.norm.cdf(2 * z0 + stats.norm.ppf(1 - alpha / 2))
    return float(p_lo), float(p_hi), float(np.quantile(boots, lo)), float(np.quantile(boots, hi))


def holm(pvals):
    p = np.asarray(pvals, dtype=float)
    order = np.argsort(p)
    n = len(p)
    adj = np.empty(n)
    running = 0.0
    for rank, idx in enumerate(order):
        running = max(running, min(1.0, p[idx] * (n - rank)))
        adj[idx] = running
    return adj


def broad(rec):
    return "negative" if "do not fund" in str(rec).lower() else "positive"


def modal(series):
    """Most frequent recommendation across iterations (ties -> most conservative)."""
    counts = series.value_counts()
    top = counts[counts == counts.max()].index.tolist()
    return sorted(top, key=REC_ORDER.index)[-1] if len(top) > 1 else top[0]


# ----------------------------------------------------------------------------- analyses
def overall_alignment(h, l, rng):
    cells = cell_means(l)
    hs = h["total_score"].to_numpy(float)
    ls = cells["total_score"].to_numpy(float)
    h_mean, h_sd = hs.mean(), hs.std(ddof=1)
    l_mean, l_sd = ls.mean(), ls.std(ddof=1)
    diff = l_mean - h_mean
    t, p = stats.ttest_ind(ls, hs)                       # LLM minus human
    glass = diff / h_sd

    def d_mean(a, b):
        return b.mean() - a.mean()

    def d_glass(a, b):
        sd = a.std(ddof=1)
        return (b.mean() - a.mean()) / sd if sd > 0 else np.nan

    ci_diff = bootstrap_ci(d_mean, hs, ls, rng)
    ci_glass = bootstrap_ci(d_glass, hs, ls, rng)

    # linear mixed-effects model (REML): individual human scores and vendor x application
    # cell means, with variance components for rater identity and application
    cols = ["total_score", "reviewer_type", "rater", "application"]
    hh = h.assign(reviewer_type="Human", rater=h["reviewer"])[cols]
    ll = cells.assign(reviewer_type="LLM", rater=cells["vendor"])[cols]
    d = pd.concat([hh, ll], ignore_index=True)
    d["reviewer_type"] = pd.Categorical(d["reviewer_type"], ["Human", "LLM"])
    d["one"] = 1
    md = smf.mixedlm("total_score ~ reviewer_type", d, groups="one",
                     vc_formula={"rater": "0 + C(rater)", "application": "0 + C(application)"})
    fit = md.fit(reml=True, method="lbfgs", maxiter=500)
    coef = "reviewer_type[T.LLM]"
    lmm = {
        "estimate": float(fit.params[coef]),
        "ci_low": float(fit.conf_int().loc[coef, 0]),
        "ci_high": float(fit.conf_int().loc[coef, 1]),
        "p_value": float(fit.pvalues[coef]),
    }
    return {
        "human_n": int(len(hs)), "llm_n_raw": int(len(l)), "llm_n_cells": int(len(ls)),
        "human_mean": h_mean, "human_sd": h_sd,
        "llm_mean": l_mean, "llm_sd": l_sd,
        "llm_mean_raw": float(l["total_score"].mean()), "llm_sd_raw": float(l["total_score"].std(ddof=1)),
        "mean_difference": diff, "diff_ci_low": ci_diff[0], "diff_ci_high": ci_diff[1],
        "diff_ci_bc": [ci_diff[2], ci_diff[3]],
        "t": float(t), "p_value": float(p),
        "glass_delta": glass, "glass_ci_low": ci_glass[0], "glass_ci_high": ci_glass[1],
        "glass_ci_bc": [ci_glass[2], ci_glass[3]],
        "mixed_model": lmm,
        "cells": cells,
    }


def criterion_level(h, l):
    rows, ps = [], []
    for col, label in CRITERIA.items():
        hs = h[col].dropna().to_numpy(float)
        cells = cell_means(l, col)[col].to_numpy(float)
        diff = float(l[col].mean() - hs.mean())         # raw LLM mean minus human mean, as reported
        t, p = stats.ttest_ind(cells, hs)
        rows.append({"criterion": label, "human_mean": hs.mean(), "llm_mean": float(l[col].mean()),
                     "difference": diff, "p_uncorrected": float(p)})
        ps.append(p)
    adj = holm(ps)
    for r, a in zip(rows, adj):
        r["p_holm"] = float(a)
    return rows


def recommendation_agreement(h, l):
    # primary: modal recommendation per vendor x application cell, paired with each human review
    cell_rec = l.groupby(["vendor", "application"])["recommendation"].agg(modal).reset_index()
    pairs = cell_rec.merge(h[["application", "reviewer", "recommendation"]], on="application",
                           suffixes=("_llm", "_human"))
    ex_llm, ex_h = pairs["recommendation_llm"], pairs["recommendation_human"]
    br_llm, br_h = ex_llm.map(broad), ex_h.map(broad)
    primary = {
        "n_pairs": int(len(pairs)),
        "exact_agreement": float((ex_llm == ex_h).mean()),
        "kappa_exact": float(cohen_kappa_score(ex_h, ex_llm)),
        "broad_agreement": float((br_llm == br_h).mean()),
        "kappa_broad": float(cohen_kappa_score(br_h, br_llm)),
    }
    # sensitivity: every raw LLM review paired with every human review of the same application
    raw = l[["application", "recommendation"]].merge(h[["application", "recommendation"]], on="application",
                                                     suffixes=("_llm", "_human"))
    sens = {
        "n_pairs": int(len(raw)),
        "kappa_exact": float(cohen_kappa_score(raw["recommendation_human"], raw["recommendation_llm"])),
        "kappa_broad": float(cohen_kappa_score(raw["recommendation_human"].map(broad), raw["recommendation_llm"].map(broad))),
    }
    dist = {
        "llm": (l["recommendation"].value_counts(normalize=True).reindex(REC_ORDER).fillna(0)).to_dict(),
        "human": (h["recommendation"].value_counts(normalize=True).reindex(REC_ORDER).fillna(0)).to_dict(),
    }
    return {"primary": primary, "sensitivity_raw_pairs": sens, "distribution": dist}


def vendor_table(h, l):
    hm = h["total_score"].mean()
    out = {}
    for v, g in l.groupby("vendor"):
        m = g["total_score"].mean()
        out[VENDOR_LABEL[v]] = {"mean": float(m), "deviation_from_human": float(m - hm)}
    return out


def dispersion(h, l):
    h_sd = h.groupby("application")["total_score"].std(ddof=1)
    l_sd = l.groupby("application")["total_score"].std(ddof=1)
    return {"human_within_app_sd_mean": float(h_sd.mean()), "llm_within_app_sd_mean": float(l_sd.mean()),
            "reduction": float(1 - l_sd.mean() / h_sd.mean())}


def application_means(h, l):
    return {"human": h.groupby("application")["total_score"].mean().round(2).to_dict(),
            "llm": l.groupby("application")["total_score"].mean().round(2).to_dict()}


def cross_experiment_anova(llm):
    groups, sizes = [], []
    for exp in EXPERIMENTS:
        l = llm[(llm["experiment"] == exp) & (llm["application"].isin(["FC1", "FC2"]))]
        g = cell_means(l)["total_score"].to_numpy(float)
        groups.append(g)
        sizes.append(len(g))
    F, p = stats.f_oneway(*groups)
    allv = np.concatenate(groups)
    ss_between = sum(len(g) * (g.mean() - allv.mean()) ** 2 for g in groups)
    ss_total = ((allv - allv.mean()) ** 2).sum()
    return {"F": float(F), "df_between": len(groups) - 1, "df_within": int(len(allv) - len(groups)),
            "p_value": float(p), "eta_squared": float(ss_between / ss_total), "group_sizes": sizes}


# ----------------------------------------------------------------------------- reporting
def write_tables(res):
    L = []
    L.append("## Table 2. Summary of experimental results across three prompt engineering conditions\n")
    hdr = "| Metric | " + " | ".join(EXPERIMENTS[e]["label"] for e in EXPERIMENTS) + " |"
    L += [hdr, "|---|" + "---|" * len(EXPERIMENTS)]

    def row(name, fn):
        L.append(f"| {name} | " + " | ".join(fn(res[e]) for e in EXPERIMENTS) + " |")

    row("Human reviews (n)", lambda r: str(r["overall"]["human_n"]))
    row("LLM reviews (n raw/aggregated)", lambda r: f"{r['overall']['llm_n_raw']}/{r['overall']['llm_n_cells']}")
    row("Human mean ± SD", lambda r: f"{r['overall']['human_mean']:.2f} ± {r['overall']['human_sd']:.2f}")
    row("LLM mean ± SD (aggregated)", lambda r: f"{r['overall']['llm_mean']:.2f} ± {r['overall']['llm_sd']:.2f}")
    row("Mean difference [95% CI]", lambda r: f"{r['overall']['mean_difference']:+.2f} [{r['overall']['diff_ci_low']:+.2f}, {r['overall']['diff_ci_high']:+.2f}]")
    row("p-value (aggregated)", lambda r: f"{r['overall']['p_value']:.3f}")
    row("Glass's Δ [95% CI]", lambda r: f"{r['overall']['glass_delta']:.2f} [{r['overall']['glass_ci_low']:.2f}, {r['overall']['glass_ci_high']:.2f}]")
    row("Broad agreement", lambda r: f"{100*r['agreement']['primary']['broad_agreement']:.1f}%")
    row("Cohen's κ (broad)", lambda r: f"{r['agreement']['primary']['kappa_broad']:.3f}")
    row("Exact agreement", lambda r: f"{100*r['agreement']['primary']['exact_agreement']:.1f}%")
    row("Cohen's κ (exact)", lambda r: f"{r['agreement']['primary']['kappa_exact']:.3f}")
    row("Mixed model: LLM effect [95% CI], p", lambda r: f"{r['overall']['mixed_model']['estimate']:+.2f} [{r['overall']['mixed_model']['ci_low']:+.2f}, {r['overall']['mixed_model']['ci_high']:+.2f}], p = {r['overall']['mixed_model']['p_value']:.3f}")
    row("Sensitivity κ, raw pairs (exact / broad)", lambda r: f"{r['agreement']['sensitivity_raw_pairs']['kappa_exact']:.3f} / {r['agreement']['sensitivity_raw_pairs']['kappa_broad']:.3f} (n = {r['agreement']['sensitivity_raw_pairs']['n_pairs']})")

    L.append("\n## Table 3. LLM vendor mean scores and deviation from human mean\n")
    L += ["| Vendor | " + " | ".join(EXPERIMENTS[e]["label"] for e in EXPERIMENTS) + " |", "|---|" + "---|" * len(EXPERIMENTS)]
    for v in VENDOR_LABEL.values():
        L.append(f"| {v} | " + " | ".join(f"{res[e]['vendors'][v]['mean']:.2f} ({res[e]['vendors'][v]['deviation_from_human']:+.2f})" for e in EXPERIMENTS) + " |")

    L.append("\n## Criterion-level deviations (LLM raw mean − human mean), t-test on cell means, Holm-corrected\n")
    for e in EXPERIMENTS:
        L.append(f"\n**{EXPERIMENTS[e]['label']}**\n")
        L += ["| Criterion | Human mean | LLM mean | Difference | p (uncorrected) | p (Holm) |", "|---|---|---|---|---|---|"]
        for r in res[e]["criteria"]:
            L.append(f"| {r['criterion']} | {r['human_mean']:.2f} | {r['llm_mean']:.2f} | {r['difference']:+.2f} | {r['p_uncorrected']:.3f} | {r['p_holm']:.3f} |")

    L.append("\n## Recommendation distributions\n")
    L += ["| Experiment | Group | Fund | Fund with Revisions | Do Not Fund |", "|---|---|---|---|---|"]
    for e in EXPERIMENTS:
        for grp in ("human", "llm"):
            d = res[e]["agreement"]["distribution"][grp]
            L.append(f"| {EXPERIMENTS[e]['label']} | {grp} | " + " | ".join(f"{100*d[k]:.1f}%" for k in REC_ORDER) + " |")

    L.append("\n## Application-level means (Figure 2) and within-application dispersion\n")
    L += ["| Experiment | Human means | LLM means | Human within-app SD | LLM within-app SD | Reduction |", "|---|---|---|---|---|---|"]
    for e in EXPERIMENTS:
        a, d = res[e]["application_means"], res[e]["dispersion"]
        L.append(f"| {EXPERIMENTS[e]['label']} | {a['human']} | {a['llm']} | {d['human_within_app_sd_mean']:.2f} | {d['llm_within_app_sd_mean']:.2f} | {100*d['reduction']:.0f}% |")

    an = res["anova_fc1_fc2"]
    L.append(f"\n## Exploratory one-way ANOVA across prompt conditions (FC1 and FC2 only)\n\nF({an['df_between']},{an['df_within']}) = {an['F']:.2f}, p = {an['p_value']:.3f}, η² = {an['eta_squared']:.3f}; group sizes {an['group_sizes']}\n")
    (OUT / "tables.md").write_text("\n".join(L) + "\n")


def main():
    rng = np.random.default_rng(SEED)
    human, llm = load()
    res = {}
    for exp in EXPERIMENTS:
        h, l = subset(human, llm, exp)
        overall = overall_alignment(h, l, rng)
        cells = overall.pop("cells")
        res[exp] = {
            "label": EXPERIMENTS[exp]["label"],
            "overall": overall,
            "criteria": criterion_level(h, l),
            "agreement": recommendation_agreement(h, l),
            "vendors": vendor_table(h, l),
            "dispersion": dispersion(h, l),
            "application_means": application_means(h, l),
            "vendor_cell_means": cells.to_dict(orient="records"),
        }
        print(f"{EXPERIMENTS[exp]['label']}: human {overall['human_mean']:.2f}±{overall['human_sd']:.2f} (n={overall['human_n']}), "
              f"LLM {overall['llm_mean']:.2f}±{overall['llm_sd']:.2f} (n={overall['llm_n_cells']}), diff {overall['mean_difference']:+.2f} "
              f"[{overall['diff_ci_low']:+.2f}, {overall['diff_ci_high']:+.2f}], p={overall['p_value']:.3f}, "
              f"Glass Δ {overall['glass_delta']:.2f} [{overall['glass_ci_low']:.2f}, {overall['glass_ci_high']:.2f}]")
    res["anova_fc1_fc2"] = cross_experiment_anova(llm)
    res["settings"] = {"seed": SEED, "n_boot": N_BOOT}

    def ser(o):
        if isinstance(o, dict):
            return {str(k): ser(v) for k, v in o.items()}
        if isinstance(o, list):
            return [ser(v) for v in o]
        if isinstance(o, (np.floating, float)):
            return None if np.isnan(o) else float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        return o

    (OUT / "results.json").write_text(json.dumps(ser(res), indent=2))
    write_tables(res)
    print(f"\nWrote {OUT / 'results.json'} and {OUT / 'tables.md'}")


if __name__ == "__main__":
    main()
