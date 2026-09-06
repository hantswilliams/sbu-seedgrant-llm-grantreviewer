#!/usr/bin/env python3
"""
Regenerate Figures 1 and 2 of the article from the de-identified data.

    Figure 1  Total score distributions by experiment: individual human scores
              (circles) and iteration-averaged LLM scores per vendor (diamonds),
              with group means and +/-1 SD bars.
    Figure 2  Application-level mean total scores across the human panel and
              the three prompt conditions (FC3 absent from Exps 2-3, where it
              served as training data).

Outputs PNG (150 dpi) and TIFF (300 dpi) files in ./output/.
Run reproduce_results.py first if you want the numbers cross-checked; this
script recomputes the plotted quantities directly from ../data/.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)

EXPERIMENTS = [
    ("exp1_zero_shot", "Exp. 1: Zero-Shot", None),
    ("exp2_few_shot", "Exp. 2: Few-Shot", "FC3"),
    ("exp3_few_shot_strict", "Exp. 3: Few-Shot + Strict", "FC3"),
]
VENDOR = {  # label and colour per vendor
    "OpenAI": ("GPT-5 Nano", "#1f77b4"),
    "Google": ("Gemini 2.5 Flash", "#e6a100"),
    "xAI": ("Grok 4 Fast", "#00a37a"),
}
HUMAN_GREY = "#555555"
APP_COLOURS = {"FC1": "#1f77b4", "FC2": "#e6a100", "FC3": "#c86aa6"}


def load():
    return pd.read_csv(DATA / "human_reviews.csv"), pd.read_csv(DATA / "llm_reviews.csv")


def figure1(human, llm):
    rng = np.random.default_rng(1)
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.6), sharey=True)
    for ax, (exp, title, train) in zip(axes, EXPERIMENTS):
        h = human if train is None else human[human["application"] != train]
        l = llm[llm["experiment"] == exp]
        if train:
            l = l[l["application"] != train]
        cells = l.groupby(["vendor", "application"], as_index=False)["total_score"].mean()

        hs = h["total_score"].to_numpy(float)
        ls = cells["total_score"].to_numpy(float)
        xh, xl = 0, 1
        ax.scatter(xh + rng.uniform(-0.12, 0.12, len(hs)), hs, s=28, color=HUMAN_GREY, zorder=3)
        for v, (lab, col) in VENDOR.items():
            sub = cells[cells["vendor"] == v]["total_score"]
            ax.scatter(xl + rng.uniform(-0.12, 0.12, len(sub)), sub, s=34, marker="D", color=col, zorder=3)
        for x, vals in ((xh, hs), (xl, ls)):
            m, sd = vals.mean(), vals.std(ddof=1)
            ax.hlines(m, x - 0.28, x + 0.28, color="black", lw=2, zorder=4)
            ax.vlines(x + 0.34, m - sd, m + sd, color="#888888", lw=1.5, zorder=2)
            ax.text(x - 0.31, m, f"{m:.1f}", ha="right", va="center", fontsize=9)
        ax.set_xticks([xh, xl])
        ax.set_xticklabels([f"Human\n(n = {len(hs)})", f"LLM aggregated\n(n = {len(ls)})"])
        ax.set_xlim(-0.7, 1.7)
        ax.set_title(title, fontsize=11)
        ax.grid(axis="y", alpha=0.3)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    axes[0].set_ylabel("Total score (0–100)")
    axes[0].set_ylim(40, 102)
    handles = [plt.Line2D([], [], marker="o", ls="", color=HUMAN_GREY, label="Human reviewer")]
    handles += [plt.Line2D([], [], marker="D", ls="", color=c, label=lab) for lab, c in VENDOR.values()]
    handles += [plt.Line2D([], [], color="black", lw=2, label="Group mean"),
                plt.Line2D([], [], color="#888888", lw=1.5, label="±1 SD")]
    fig.legend(handles=handles, loc="lower center", ncol=6, frameon=False, fontsize=9, bbox_to_anchor=(0.5, -0.02))
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(OUT / "figure1_score_distributions.png", dpi=150, bbox_inches="tight")
    fig.savefig(OUT / "figure1_score_distributions.tiff", dpi=300, bbox_inches="tight")
    plt.close(fig)


def figure2(human, llm):
    conds = ["Human"] + [e[0] for e in EXPERIMENTS]
    labels = ["Human", "Zero-Shot", "Few-Shot", "Few-Shot\n+ Strict"]
    means = {app: [] for app in ("FC1", "FC2", "FC3")}
    for app in means:
        means[app].append(human[human["application"] == app]["total_score"].mean())
        for exp, _, train in EXPERIMENTS:
            if train == app:
                means[app].append(np.nan)
            else:
                means[app].append(llm[(llm["experiment"] == exp) & (llm["application"] == app)]["total_score"].mean())
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(len(conds))
    for app, vals in means.items():
        vals = np.array(vals, float)
        ax.plot(x, vals, marker="o", lw=2, color=APP_COLOURS[app], label=app)
        off = {"FC1": (0, 8), "FC2": (0, -14), "FC3": (0, -14)}[app]
        for xi, v in zip(x, vals):
            if np.isfinite(v):
                ax.annotate(f"{v:.1f}", (xi, v), textcoords="offset points", xytext=off, ha="center", fontsize=9, color="#333333")
        last = np.where(np.isfinite(vals))[0][-1]
        ax.annotate(app, (x[last], vals[last]), textcoords="offset points", xytext=(8, -4), fontsize=10, color=APP_COLOURS[app], weight="bold")
    ax.text(0.02, 0.04, "FC3 excluded from Experiments 2–3 (training data)", transform=ax.transAxes, fontsize=9, style="italic", color="#666666")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Mean total score (0–100)")
    ax.set_ylim(60, 95)
    ax.grid(axis="y", alpha=0.3)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "figure2_rank_ordering.png", dpi=150)
    fig.savefig(OUT / "figure2_rank_ordering.tiff", dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    human, llm = load()
    figure1(human, llm)
    figure2(human, llm)
    print(f"Figures written to {OUT}")
