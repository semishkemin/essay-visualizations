"""Show a published prevalence estimate as an editorial statistic card."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


# 1. Palette
BACKGROUND = "#EFE8DC"
CARD = "#F8F5EF"
INK = "#233238"
MUTED = "#687478"
ACCENT = "#2F6F73"
CI_COLOR = "#B9CCC6"
RULE = "#D3C8B9"


# 2. Output settings
OUTPUT_DIR = Path(__file__).resolve().parent / "figures"
OUTPUT_NAME = "03_prevalence"

EXPORT_WIDTH_PX = 650


# 3. Published values from Lundorff et al. (2017)
# Values are percentages, not proportions or simulated observations.
ESTIMATE = 9.8
CI_LOW = 6.8
CI_HIGH = 14.0


def main():
    # 4. Typography
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "text.color": INK,
        "axes.labelcolor": INK,
        "xtick.color": MUTED,
        "svg.fonttype": "none",
    })

    # 5. Canvas
    fig = plt.figure(
        figsize=(6.5, 4.2),
        facecolor=BACKGROUND,
    )

    # Kicker
    fig.text(
        0.07, 0.925,
        "PUBLISHED PREVALENCE ESTIMATE",
        fontsize=8.5,
        weight="bold",
        color=ACCENT,
    )

    # Main title
    fig.text(
        0.07, 0.855,
        "How common is prolonged grief disorder?",
        fontsize=17,
        weight="bold",
        color=INK,
    )

    # Study context
    fig.text(
        0.07, 0.805,
        "Adults after non-violent bereavement  ·  14 studies  ·  2017 meta-analysis",
        fontsize=8.5,
        color=MUTED,
    )

    # 6. Main statistic
    fig.text(
        0.07, 0.655,
        f"{ESTIMATE:.1f}%",
        fontsize=30,
        weight="bold",
        color=ACCENT,
    )

    fig.text(
        0.30, 0.682,
        "pooled prevalence",
        fontsize=11,
        weight="bold",
        color=INK,
    )

    fig.text(
        0.30, 0.642,
        "across included studies",
        fontsize=9,
        color=MUTED,
    )

    # 7. Confidence interval card
    ax = fig.add_axes([0.07, 0.355, 0.86, 0.20])

    ax.set_xlim(0, 20)
    ax.set_ylim(-1, 1)
    ax.axis("off")

    card = FancyBboxPatch(
        (0, 0),
        1,
        1,
        transform=ax.transAxes,
        boxstyle="round,pad=0.018,rounding_size=0.035",
        facecolor=CARD,
        edgecolor="none",
        clip_on=False,
        zorder=0,
    )
    ax.add_patch(card)

    # Small CI heading
    ax.text(
        0.04, 0.79,
        "95% CONFIDENCE INTERVAL",
        transform=ax.transAxes,
        fontsize=7.5,
        weight="bold",
        color=MUTED,
        va="center",
    )

    # Full reference scale
    ax.plot(
        [2, 18],
        [0, 0],
        color=RULE,
        linewidth=1.2,
        zorder=1,
    )

    # Confidence interval
    ax.plot(
        [CI_LOW, CI_HIGH],
        [0, 0],
        color=CI_COLOR,
        linewidth=11,
        solid_capstyle="round",
        zorder=2,
    )

    # Point estimate
    ax.scatter(
        ESTIMATE,
        0,
        s=180,
        facecolor=ACCENT,
        edgecolor=CARD,
        linewidth=2.5,
        zorder=3,
    )

    # Endpoint markers
    for endpoint in (CI_LOW, CI_HIGH):
        ax.plot(
            [endpoint, endpoint],
            [-0.15, 0.15],
            color=INK,
            linewidth=1.4,
            zorder=3,
        )

    # Endpoint labels
    ax.text(
        CI_LOW,
        -0.38,
        f"{CI_LOW:.1f}%",
        ha="center",
        va="top",
        fontsize=8.5,
        weight="bold",
        color=INK,
    )

    ax.text(
        CI_HIGH,
        -0.38,
        f"{CI_HIGH:.1f}%",
        ha="center",
        va="top",
        fontsize=8.5,
        weight="bold",
        color=INK,
    )

    # Estimate label
    ax.text(
        ESTIMATE,
        0.40,
        f"{ESTIMATE:.1f}%",
        ha="center",
        va="bottom",
        fontsize=9.5,
        weight="bold",
        color=ACCENT,
    )

    # 8. Interpretation note
    fig.text(
        0.07, 0.255,
        "Interpret with care.",
        fontsize=9.5,
        weight="bold",
        color=INK,
    )

    fig.text(
        0.07, 0.205,
        "Study criteria and samples varied. This estimate cannot be directly",
        fontsize=8,
        color=MUTED,
    )

    fig.text(
        0.07, 0.173,
        "generalized to all losses or to current diagnostic criteria.",
        fontsize=8,
        color=MUTED,
    )

    # 9. Source
    fig.text(
        0.07, 0.085,
        "Lundorff et al. · Journal of Affective Disorders · 2017 · 212:138–149",
        fontsize=7.5,
        color=MUTED,
    )

    fig.text(
        0.07, 0.055,
        "doi:10.1016/j.jad.2017.01.030",
        fontsize=7,
        color=MUTED,
    )

    # 10. Export
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    export_dpi = EXPORT_WIDTH_PX / fig.get_figwidth()

    # PNG: exactly 650 px wide
    png_path = OUTPUT_DIR / f"{OUTPUT_NAME}.png"

    fig.savefig(
        png_path,
        dpi=export_dpi,
        facecolor=BACKGROUND,
        transparent=False,
    )

    print(f"Saved: {png_path}")

    # SVG stays vector-based
    svg_path = OUTPUT_DIR / f"{OUTPUT_NAME}.svg"

    fig.savefig(
        svg_path,
        facecolor=BACKGROUND,
        transparent=False,
    )

    print(f"Saved: {svg_path}")

    plt.close(fig)


if __name__ == "__main__":
    main()