"""Draw a shared diagnostic timeline with milestone cards."""

# 1. Imports
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


# 2. Colors and output settings
COLORS = {
    "background": "#EDE2CC",
    "ink": "#24343A",
    "muted": "#59676B",
    "card": "#FAF6EE",
    "icd": "#236B70",
    "dsm": "#566A91",
}

OUTPUT_DIR = Path(__file__).resolve().parent / "figures"
OUTPUT_NAME = "02_diagnostic_timeline_milestones"


# 3. Reusable milestone card
def draw_card(ax, center, bottom, width, title, subtitle, color):
    left = center - width / 2

    box = FancyBboxPatch(
        (left, bottom),
        width,
        1.35,
        boxstyle="round,pad=0.10,rounding_size=0.12",
        facecolor=COLORS["card"],
        edgecolor=color,
        linewidth=1.8,
        alpha=1,
        zorder=4,
    )
    ax.add_patch(box)

    ax.text(
        center, bottom + 0.86,
        title,
        ha="center",
        va="center",
        fontsize=17,
        weight="bold",
        color=color,
        zorder=5,
    )

    ax.text(
        center, bottom + 0.35,
        subtitle,
        ha="center",
        va="center",
        fontsize=11,
        color=COLORS["ink"],
        zorder=5,
    )


def main():
    # 4. Canvas and headings
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "svg.fonttype": "none",
    })

    fig = plt.figure(
        figsize=(12, 8),
        facecolor=COLORS["background"],
    )

    fig.text(
        0.065, 0.925,
        "THE MEDICALIZATION OF GRIEF",
        fontsize=10,
        weight="bold",
        color=COLORS["icd"],
    )

    fig.text(
        0.065, 0.855,
        "When does a diagnosis become possible?",
        fontsize=25,
        weight="bold",
        color=COLORS["ink"],
    )

    fig.text(
        0.065, 0.805,
        "Time thresholds for prolonged grief disorder",
        fontsize=13,
        color=COLORS["muted"],
    )

    ax = fig.add_axes([0.065, 0.28, 0.87, 0.47])
    ax.set(xlim=(-1.3, 16), ylim=(0, 8))
    ax.axis("off")

    axis_y = 4.2

    # 5. Shared time arrow and monthly ticks
    ax.annotate(
        "",
        xy=(15.5, axis_y),
        xytext=(0, axis_y),
        arrowprops={
            "arrowstyle": "-|>",
            "color": COLORS["ink"],
            "lw": 4,
            "mutation_scale": 22,
        },
        zorder=2,
    )

    for month in range(1, 15):
        if month not in (6, 12):
            ax.plot(
                [month, month],
                [axis_y - 0.09, axis_y + 0.09],
                color=COLORS["ink"],
                lw=1.4,
                zorder=2,
            )

    # 6. Milestones
    milestones = [
        (0, "The loss"),
        (6, "6 months"),
        (12, "12 months"),
    ]

    for month, label in milestones:
        ax.scatter(
            month, axis_y,
            s=220,
            facecolor=COLORS["background"],
            edgecolor=COLORS["ink"],
            linewidth=3,
            zorder=3,
        )

        ax.text(
            month, axis_y - 0.65,
            label,
            ha="center",
            va="center",
            fontsize=16 if month else 12,
            weight="bold",
            color=COLORS["ink"],
        )

    # 7. Upper cards and connectors
    upper_cards = [
        (6, "ICD-11", "All ages*", COLORS["icd"]),
        (12, "DSM-5-TR", "Adults", COLORS["dsm"]),
    ]

    for month, title, subtitle, color in upper_cards:
        ax.plot(
            [month, month],
            [axis_y + 0.18, 5.75],
            color=color,
            lw=2.5,
            zorder=1,
        )

        draw_card(
            ax,
            center=month,
            bottom=5.75,
            width=4.0,
            title=title,
            subtitle=subtitle,
            color=color,
        )

    # 8. Lower card at the shared six-month milestone
    ax.plot(
        [6, 6],
        [axis_y - 0.18, 2.7],
        color=COLORS["dsm"],
        lw=2.5,
        zorder=1,
    )

    # Opaque backing prevents the connector from crossing the label.
    ax.text(
        6, axis_y - 0.65,
        "6 months",
        ha="center",
        va="center",
        fontsize=16,
        weight="bold",
        color=COLORS["ink"],
        zorder=6,
        bbox={
            "facecolor": COLORS["background"],
            "edgecolor": "none",
            "pad": 4,
        },
    )

    draw_card(
        ax,
        center=6,
        bottom=1.25,
        width=5.2,
        title="DSM-5-TR",
        subtitle="Children and adolescents",
        color=COLORS["dsm"],
    )

    ax.text(
        15.4, axis_y - 0.65,
        "Time since loss",
        ha="right",
        va="center",
        fontsize=10,
        color=COLORS["muted"],
    )

    # 9. Interpretation and sources
    fig.text(
        0.065, 0.24,
        "These are not deadlines for grief.",
        fontsize=17,
        weight="bold",
        color=COLORS["ink"],
    )

    fig.text(
        0.065, 0.195,
        "Time alone is not enough: symptoms, impairment, "
        "and cultural context also matter.",
        fontsize=11,
        color=COLORS["muted"],
    )

    fig.text(
        0.065, 0.152,
        "*ICD-11 uses a six-month minimum; "
        "cultural expectations may require longer.",
        fontsize=10,
        color=COLORS["muted"],
    )

    fig.text(
        0.065, 0.11,
        "Support can be sought before these thresholds.",
        fontsize=11,
        color=COLORS["icd"],
    )

    fig.text(
        0.065, 0.055,
        "Sources: WHO, ICD-11 (6B42); APA, Prolonged Grief Disorder "
        "(reviewed August 2025).",
        fontsize=8,
        color=COLORS["muted"],
    )

    # 10. Fully opaque exports
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for extension in ("png", "svg"):
        path = OUTPUT_DIR / f"{OUTPUT_NAME}.{extension}"

        fig.savefig(
            path,
            dpi=650 / 12,
            facecolor=COLORS["background"],
            transparent=False,
        )

        print(f"Saved: {path}")

    plt.close(fig)


if __name__ == "__main__":
    main()