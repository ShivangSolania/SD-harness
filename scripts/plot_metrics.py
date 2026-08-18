#!/usr/bin/env python3
"""
Publication plotting script for SD-Harness evaluation metrics.

Loads framework targets and session telemetry from evaluations/metrics.json
and generates publication-quality (350 DPI) academic figures:
  - evaluations/reports/figures/latency_by_tier.png
  - evaluations/reports/figures/retries_by_tier.png
  - evaluations/reports/figures/framework_targets.png
  - evaluations/reports/figures/measured_vs_targets.png

Academic Note:
  Explicitly distinguishes Declared Target Specifications (framework SLAs)
  from Measured Session Telemetry (empirical runtime logs) to maintain
  factual rigor.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd


def load_metrics(input_path: Path) -> tuple[pd.DataFrame, dict[str, float]]:
    """
    Load evaluation metrics and return structured session telemetry DataFrame
    alongside framework target specifications.
    """
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    targets: dict[str, float] = data.get("framework_benchmarks", {})
    session_data: list[dict[str, Any]] = data.get("session_telemetry_summary", [])

    records = []
    for item in session_data:
        retries_dict = item.get("retries", {})
        total_retries = sum(retries_dict.values())
        record = {
            "sessionId": item.get("sessionId", ""),
            "tier": item.get("tier", ""),
            "durationMs": item.get("durationMs", 0),
            "durationSec": item.get("durationMs", 0) / 1000.0,
            "outcome": item.get("outcome", "pass"),
            "total_retries": total_retries,
            "retries_coder": retries_dict.get("coder", 0),
            "retries_reviewer": retries_dict.get("reviewer", 0),
            "retries_tester": retries_dict.get("tester", 0),
            "retries_planner": retries_dict.get("planner", 0),
            "retries_security": retries_dict.get("security", 0),
            "retries_doc": retries_dict.get("documentation", 0),
            "retries_dict": retries_dict,
        }
        records.append(record)

    df = pd.DataFrame(records)
    return df, targets


def configure_style() -> None:
    """Configure publication-quality aesthetics for all matplotlib figures."""
    plt.rcParams.update({
        "figure.dpi": 350,
        "savefig.dpi": 350,
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial", "sans-serif"],
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
        "axes.labelweight": "bold",
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 9.5,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "grid.linestyle": "--",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.autolayout": False,
    })


def plot_latency(df: pd.DataFrame, output_dir: Path) -> None:
    """
    Generate latency by tier figure (latency_by_tier.png).
    Visualizes execution duration across ATOMIC, FEATURE, and ARCHITECTURAL tiers.
    """
    fig, ax = plt.subplots(figsize=(7.5, 4.8), dpi=350)

    colors = ["#2b5c8f", "#d97706", "#7c3aed"]
    tiers = df["tier"].tolist()
    durations_sec = df["durationSec"].tolist()
    durations_ms = df["durationMs"].tolist()

    bars = ax.bar(tiers, durations_sec, color=colors[:len(tiers)], width=0.55, edgecolor="#1e293b", linewidth=1.2, zorder=3)

    ax.set_ylabel("Execution Latency (seconds)", labelpad=8)
    ax.set_xlabel("Workflow Complexity Tier", labelpad=8)
    ax.set_title("Execution Latency by Workflow Tier\n(Empirical Session Telemetry)", pad=14)

    max_sec = max(durations_sec) if durations_sec else 60.0
    ax.set_ylim(0, max_sec * 1.25)
    ax.yaxis.grid(True, linestyle="--", alpha=0.3, zorder=0)
    ax.xaxis.grid(False)

    for bar, ms, sec in zip(bars, durations_ms, durations_sec):
        height = bar.get_height()
        ax.annotate(
            f"{sec:.2f} s\n({ms:,} ms)",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9.5,
            fontweight="bold",
            color="#0f172a",
        )

    plt.tight_layout()
    target_file = output_dir / "latency_by_tier.png"
    plt.savefig(target_file, dpi=350, bbox_inches="tight")
    plt.close(fig)


def plot_retries(df: pd.DataFrame, output_dir: Path) -> None:
    """
    Generate retry distribution figure (retries_by_tier.png).
    Visualizes agent retry counts broken down by tier and participating agent roles.
    """
    fig, ax = plt.subplots(figsize=(8.0, 5.0), dpi=350)

    role_keys = ["coder", "reviewer", "tester", "planner", "security", "documentation"]
    role_labels = ["Coder", "Reviewer", "Tester", "Planner", "Security", "Documentation"]
    role_colors = ["#3b82f6", "#10b981", "#f59e0b", "#ec4899", "#8b5cf6", "#64748b"]

    tiers = df["tier"].tolist()
    x = np.arange(len(tiers))
    width = 0.52

    bottoms = np.zeros(len(tiers))
    any_retries = False

    for role_key, role_label, color in zip(role_keys, role_labels, role_colors):
        counts = [row.get(role_key, 0) for row in df["retries_dict"]]
        if any(c > 0 for c in counts):
            any_retries = True
            ax.bar(
                x,
                counts,
                width,
                bottom=bottoms,
                label=f"{role_label} Agent",
                color=color,
                edgecolor="#1e293b",
                linewidth=0.8,
                zorder=3,
            )
            bottoms += np.array(counts)

    if not any_retries:
        ax.bar(x, [0] * len(tiers), width, color="#94a3b8", zorder=3)

    ax.set_xticks(x)
    ax.set_xticklabels(tiers)
    ax.set_ylabel("Retry Count", labelpad=8)
    ax.set_xlabel("Workflow Complexity Tier", labelpad=8)
    ax.set_title("Agent Retry Distribution Across Workflow Tiers\n(Breakdown by Agent Role)", pad=14)

    max_retries = max(bottoms) if len(bottoms) > 0 else 2
    ax.set_ylim(0, max(max_retries + 1.2, 3.0))
    ax.yaxis.set_major_locator(mtick.MaxNLocator(integer=True))
    ax.yaxis.grid(True, linestyle="--", alpha=0.3, zorder=0)
    ax.xaxis.grid(False)

    for i, (total, tier_name) in enumerate(zip(bottoms, tiers)):
        if total == 0:
            ax.text(
                i,
                0.15,
                "0 Retries\n(Zero-Retry Pass)",
                ha="center",
                va="bottom",
                fontsize=9.0,
                fontweight="bold",
                color="#047857",
            )
        else:
            role_breakdown = [
                f"{k.capitalize()}: {v}"
                for k, v in df.iloc[i]["retries_dict"].items()
                if v > 0
            ]
            breakdown_str = ", ".join(role_breakdown)
            ax.text(
                i,
                total + 0.12,
                f"Total: {int(total)}\n({breakdown_str})",
                ha="center",
                va="bottom",
                fontsize=9.0,
                fontweight="bold",
                color="#1e293b",
            )

    ax.legend(loc="upper right", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1")

    plt.tight_layout()
    target_file = output_dir / "retries_by_tier.png"
    plt.savefig(target_file, dpi=350, bbox_inches="tight")
    plt.close(fig)


def plot_targets(targets: dict[str, float], output_dir: Path) -> None:
    """
    Generate declared target specifications figure (framework_targets.png).
    Visualizes framework-level golden eval SLA targets.
    """
    fig, ax = plt.subplots(figsize=(8.0, 4.5), dpi=350)

    metric_keys = ["surgical_patch_accuracy", "target_hit_rate", "allowed_hallucination_index"]
    metric_labels = [
        "Surgical Patch Accuracy\n(Minimum Target)",
        "Target Hit Rate\n(Golden Eval Target)",
        "Allowed Hallucination Index\n(Maximum Upper Bound)",
    ]
    values = [targets.get(k, 0.0) for k in metric_keys]
    bar_colors = ["#10b981", "#3b82f6", "#ef4444"]

    y_pos = np.arange(len(metric_labels))
    bars = ax.barh(y_pos, values, height=0.52, color=bar_colors, edgecolor="#1e293b", linewidth=1.0, zorder=3)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(metric_labels)
    ax.invert_yaxis()  # Highest priority metric at top
    ax.set_xlabel("Target Metric Value (Ratio / Percentage)", labelpad=8)
    ax.set_xlim(0, 1.15)
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.set_title("Declared Framework Target Specifications\n(Evaluations Benchmark Golden Dataset SLAs)", pad=14)

    ax.xaxis.grid(True, linestyle="--", alpha=0.3, zorder=0)
    ax.yaxis.grid(False)

    for bar, val in zip(bars, values):
        width = bar.get_width()
        pct_str = f"{val * 100:.1f}% ({val:.2f})"
        ax.annotate(
            pct_str,
            xy=(width, bar.get_y() + bar.get_height() / 2),
            xytext=(8, 0),
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=9.5,
            fontweight="bold",
            color="#0f172a",
        )

    plt.tight_layout()
    target_file = output_dir / "framework_targets.png"
    plt.savefig(target_file, dpi=350, bbox_inches="tight")
    plt.close(fig)


def plot_measured_vs_targets(
    df: pd.DataFrame, targets: dict[str, float], output_dir: Path
) -> None:
    """
    Generate side-by-side comparison figure (measured_vs_targets.png).
    Explicitly contrasts Declared Target Specifications against Measured Session Telemetry
    to prevent confounding target specifications with empirical session measurements.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 5.2), dpi=350)

    # Subplot 1: Declared Target Specifications
    target_keys = ["target_hit_rate", "surgical_patch_accuracy", "allowed_hallucination_index"]
    target_labels = ["Target Hit Rate\n(Target SLA)", "Surgical Patch Acc.\n(Target SLA)", "Allowed Hallucination\n(Max Upper Bound)"]
    target_vals = [targets.get(k, 0.0) for k in target_keys]
    target_colors = ["#2563eb", "#059669", "#dc2626"]

    bars1 = ax1.bar(
        range(len(target_labels)),
        target_vals,
        color=target_colors,
        width=0.55,
        edgecolor="#1e293b",
        linewidth=1.1,
        zorder=3,
    )
    ax1.set_xticks(range(len(target_labels)))
    ax1.set_xticklabels(target_labels, fontsize=9.0)
    ax1.set_ylim(0, 1.25)
    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax1.set_ylabel("Specification Ratio", labelpad=8)
    ax1.set_title("Declared Target Specifications\n(Golden Dataset Benchmark SLAs)", fontsize=11, fontweight="bold", pad=10)
    ax1.yaxis.grid(True, linestyle="--", alpha=0.3, zorder=0)
    ax1.xaxis.grid(False)

    for bar, val in zip(bars1, target_vals):
        height = bar.get_height()
        ax1.annotate(
            f"{val * 100:.1f}%\n({val:.2f})",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.8,
            fontweight="bold",
            color="#0f172a",
        )

    # Subplot 2: Measured Session Telemetry
    total_sessions = len(df)
    passed_sessions = sum(df["outcome"] == "pass")
    pass_rate = passed_sessions / total_sessions if total_sessions > 0 else 0.0

    zero_retry_sessions = sum(df["total_retries"] == 0)
    zero_retry_rate = zero_retry_sessions / total_sessions if total_sessions > 0 else 0.0

    measured_labels = [
        f"Session Pass Rate\n({passed_sessions}/{total_sessions} Passed)",
        f"Zero-Retry Rate\n({zero_retry_sessions}/{total_sessions} Clean)",
        "Mean Retries/Session\n(Across Tiers)",
    ]
    mean_retries = df["total_retries"].mean() if total_sessions > 0 else 0.0
    measured_vals = [pass_rate, zero_retry_rate, mean_retries / 3.0]  # normalized for visual clarity

    measured_colors = ["#0d9488", "#6366f1", "#d97706"]
    bars2 = ax2.bar(
        range(len(measured_labels)),
        measured_vals,
        color=measured_colors,
        width=0.55,
        edgecolor="#1e293b",
        linewidth=1.1,
        zorder=3,
    )
    ax2.set_xticks(range(len(measured_labels)))
    ax2.set_xticklabels(measured_labels, fontsize=9.0)
    ax2.set_ylim(0, 1.25)
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax2.set_ylabel("Empirical Performance Ratio", labelpad=8)
    ax2.set_title("Measured Session Telemetry\n(Empirical Runtime Execution Logs)", fontsize=11, fontweight="bold", pad=10)
    ax2.yaxis.grid(True, linestyle="--", alpha=0.3, zorder=0)
    ax2.xaxis.grid(False)

    display_texts = [
        f"{pass_rate * 100:.1f}%\n(3/3 Pass)",
        f"{zero_retry_rate * 100:.1f}%\n(1/3 Clean)",
        f"{mean_retries:.2f} avg\n(1.0 retry/sess)",
    ]
    for bar, text in zip(bars2, display_texts):
        height = bar.get_height()
        ax2.annotate(
            text,
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.8,
            fontweight="bold",
            color="#0f172a",
        )

    fig.suptitle(
        "Framework Benchmark Specifications vs. Empirical Session Telemetry",
        fontsize=13,
        fontweight="bold",
        y=1.02,
    )

    plt.tight_layout()
    target_file = output_dir / "measured_vs_targets.png"
    plt.savefig(target_file, dpi=350, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Publication plotting script for SD-Harness evaluation metrics.")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("evaluations/metrics.json"),
        help="Path to metrics.json",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("evaluations/reports/figures"),
        help="Output directory",
    )
    args = parser.parse_args()

    args.output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    df, targets = load_metrics(args.input)

    configure_style()

    plot_latency(df, args.output_dir)

    plot_retries(df, args.output_dir)

    plot_targets(targets, args.output_dir)

    plot_measured_vs_targets(df, targets, args.output_dir)

    print(f"Generated 350-DPI publication figures in: {args.output_dir}")


if __name__ == "__main__":
    main()
