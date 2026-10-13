from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch


WIDTH_PX = 500
HEIGHT_PX = 500
DPI = 100

OUTPUT_DIR = Path("output")
OUTPUT_FILE = OUTPUT_DIR / "how_stigma_travels.png"


# PALETTE


BACKGROUND = "#F5F1E8"
BOX_FILL = "#E8DECC"
CENTER_FILL = "#D8C7A8"
BORDER = "#A08C72"
TITLE = "#3E342A"
BODY = "#4B4137"
SOURCE = "#9A8871"


# FIGURE


fig = plt.figure(
    figsize=(WIDTH_PX / DPI, HEIGHT_PX / DPI),
    dpi=DPI,
    facecolor=BACKGROUND,
)

ax = fig.add_axes([0, 0, 1, 1])

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect("equal")
ax.axis("off")
ax.set_facecolor(BACKGROUND)



# TITLE


ax.text(
    0.5,
    0.935,
    "HOW STIGMA TRAVELS",
    ha="center",
    va="center",
    fontsize=14,
    fontweight="bold",
    color=TITLE,
)



# HELPERS


def add_box(x, y, width, height, heading, body):

    patch = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.010,rounding_size=0.024",
        linewidth=1.35,
        edgecolor=BORDER,
        facecolor=BOX_FILL,
        zorder=3,
    )

    ax.add_patch(patch)

    ax.text(
        x + width / 2,
        y + height * 0.68,
        heading,
        ha="center",
        va="center",
        fontsize=8.8,
        fontweight="bold",
        color=TITLE,
        linespacing=1.0,
        zorder=4,
    )

    ax.text(
        x + width / 2,
        y + height * 0.34,
        body,
        ha="center",
        va="center",
        fontsize=7.7,
        color=BODY,
        linespacing=1.20,
        zorder=4,
    )

    return {
        "x": x,
        "y": y,
        "w": width,
        "h": height,
        "left": x,
        "right": x + width,
        "bottom": y,
        "top": y + height,
    }


def point_on_circle_toward(point, center, radius):
    """
    Finds the exact point where a line from the box toward
    the centre intersects the circle boundary.
    """

    px, py = point
    cx, cy = center

    dx = px - cx
    dy = py - cy

    length = (dx * dx + dy * dy) ** 0.5

    return (
        cx + radius * dx / length,
        cy + radius * dy / length,
    )


def draw_arrow(start, end):
    """
    Connector begins exactly at the box boundary.
    Arrowhead terminates exactly at the circle boundary.
    """

    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops={
            "arrowstyle": "-|>",
            "color": BORDER,
            "linewidth": 1.25,
            "mutation_scale": 10,
            "shrinkA": 0,
            "shrinkB": 0,
        },
        zorder=2,
    )



# BOXES


BOX_W = 0.295
BOX_H = 0.150


public_box = add_box(
    0.085,
    0.705,
    BOX_W,
    BOX_H,
    "PUBLIC STIGMA",
    "Staring · comments\navoidance · pity",
)


self_box = add_box(
    0.620,
    0.705,
    BOX_W,
    BOX_H,
    "SELF-STIGMA",
    "Self-consciousness\nanticipating judgment",
)


association_box = add_box(
    0.085,
    0.190,
    BOX_W,
    BOX_H,
    "STIGMA BY\nASSOCIATION",
    "Parents · partners\nfamily",
)


structural_box = add_box(
    0.620,
    0.190,
    BOX_W,
    BOX_H,
    "STRUCTURAL\nSTIGMA",
    "Work · services\nmedia · institutions",
)


# CENTRAL CIRCLE


CENTER = (0.5, 0.465)
RADIUS = 0.105


circle = Circle(
    CENTER,
    RADIUS,
    facecolor=CENTER_FILL,
    edgecolor=BORDER,
    linewidth=1.35,
    zorder=3,
)

ax.add_patch(circle)


ax.text(
    CENTER[0],
    CENTER[1],
    "VISIBLE\nDIFFERENCE",
    ha="center",
    va="center",
    fontsize=9.6,
    fontweight="bold",
    color=TITLE,
    linespacing=1.0,
    zorder=4,
)



# ARROWS


connections = [

    # PUBLIC STIGMA
    (
        (
            public_box["right"],
            public_box["bottom"],
        ),
        point_on_circle_toward(
            (
                public_box["right"],
                public_box["bottom"],
            ),
            CENTER,
            RADIUS,
        ),
    ),

    # SELF-STIGMA
    (
        (
            self_box["left"],
            self_box["bottom"],
        ),
        point_on_circle_toward(
            (
                self_box["left"],
                self_box["bottom"],
            ),
            CENTER,
            RADIUS,
        ),
    ),

    # STIGMA BY ASSOCIATION
    (
        (
            association_box["right"],
            association_box["top"],
        ),
        point_on_circle_toward(
            (
                association_box["right"],
                association_box["top"],
            ),
            CENTER,
            RADIUS,
        ),
    ),

    # STRUCTURAL STIGMA
    (
        (
            structural_box["left"],
            structural_box["top"],
        ),
        point_on_circle_toward(
            (
                structural_box["left"],
                structural_box["top"],
            ),
            CENTER,
            RADIUS,
        ),
    ),
]


for start, end in connections:
    draw_arrow(start, end)



# SOURCE


ax.text(
    0.5,
    0.065,
    "Adapted from Rasset et al. (2022), Body Image, 43, 450–462.",
    ha="center",
    va="center",
    fontsize=6.5,
    color=SOURCE,
)


OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

fig.savefig(
    OUTPUT_FILE,
    dpi=DPI,
    facecolor=BACKGROUND,
    bbox_inches=None,
    pad_inches=0,
)

plt.close(fig)

print(f"Saved: {OUTPUT_FILE.resolve()}")