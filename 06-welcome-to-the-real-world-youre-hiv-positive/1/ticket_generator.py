import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH = 1456
HEIGHT = 1048

BG_COLOR = (20, 20, 20)
TICKET_COLOR = (235, 228, 205)
TEXTURE_COLOR = (215, 205, 180)
INK_COLOR = (40, 40, 45)
BLOOD_COLOR = (130, 0, 0)


def load_font(primary_font, fallback_font, size):
    """Load the preferred font, with a portable fallback."""
    try:
        return ImageFont.truetype(primary_font, size)
    except OSError:
        try:
            return ImageFont.truetype(fallback_font, size)
        except OSError:
            return ImageFont.load_default()


def create_ticket(
    output_path="cinema_ticket_vintage.png",
    seed=42,
):
    """Create the vintage cinema-ticket illustration used in the essay."""

    random.seed(seed)

    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    main_font = load_font(
        "courbd.ttf",
        "DejaVuSansMono-Bold.ttf",
        90,
    )

    sub_font = load_font(
        "cour.ttf",
        "DejaVuSansMono.ttf",
        45,
    )

    vintage_font = load_font(
        "cour.ttf",
        "DejaVuSansMono.ttf",
        50,
    )

    ticket_w = 1300
    ticket_h = 650

    ticket_x = (WIDTH - ticket_w) // 2
    ticket_y = (HEIGHT - ticket_h) // 2

    # Shadow
    shadow_offset = 20

    draw.rectangle(
        [
            ticket_x + shadow_offset,
            ticket_y + shadow_offset,
            ticket_x + ticket_w + shadow_offset,
            ticket_y + ticket_h + shadow_offset,
        ],
        fill=(5, 5, 5),
    )

    # Ticket body
    draw.rectangle(
        [
            ticket_x,
            ticket_y,
            ticket_x + ticket_w,
            ticket_y + ticket_h,
        ],
        fill=TICKET_COLOR,
    )

    # Paper texture
    for _ in range(60000):
        nx = random.randint(ticket_x, ticket_x + ticket_w - 1)
        ny = random.randint(ticket_y, ticket_y + ticket_h - 1)
        draw.point((nx, ny), fill=TEXTURE_COLOR)

    # Perforation
    tear_x = ticket_x + 950

    for y in range(ticket_y, ticket_y + ticket_h, 30):
        draw.line(
            [(tear_x, y), (tear_x, y + 15)],
            fill=(170, 160, 140),
            width=4,
        )

    # Ticket cut-outs
    radius = 45

    draw.ellipse(
        [
            ticket_x - radius,
            ticket_y + (ticket_h // 2) - radius,
            ticket_x + radius,
            ticket_y + (ticket_h // 2) + radius,
        ],
        fill=BG_COLOR,
    )

    draw.ellipse(
        [
            ticket_x + ticket_w - radius,
            ticket_y + (ticket_h // 2) - radius,
            ticket_x + ticket_w + radius,
            ticket_y + (ticket_h // 2) + radius,
        ],
        fill=BG_COLOR,
    )

    draw.ellipse(
        [
            tear_x - radius,
            ticket_y - radius,
            tear_x + radius,
            ticket_y + radius,
        ],
        fill=BG_COLOR,
    )

    draw.ellipse(
        [
            tear_x - radius,
            ticket_y + ticket_h - radius,
            tear_x + radius,
            ticket_y + ticket_h + radius,
        ],
        fill=BG_COLOR,
    )

    # Main ticket text
    draw.text(
        (ticket_x + 100, ticket_y + 100),
        "ADMIT ONE",
        fill=INK_COLOR,
        font=main_font,
    )

    draw.text(
        (ticket_x + 100, ticket_y + 220),
        "WELCOME TO THE REAL WORLD",
        fill=INK_COLOR,
        font=sub_font,
    )

    draw.text(
        (ticket_x + 100, ticket_y + 380),
        "DATE: 1998",
        fill=INK_COLOR,
        font=vintage_font,
    )

    draw.text(
        (ticket_x + 100, ticket_y + 460),
        "ROW : H",
        fill=INK_COLOR,
        font=vintage_font,
    )

    draw.text(
        (ticket_x + 100, ticket_y + 540),
        "SEAT: 14",
        fill=INK_COLOR,
        font=vintage_font,
    )

    # Stub text
    draw.text(
        (tear_x + 80, ticket_y + 160),
        "STUB",
        fill=INK_COLOR,
        font=vintage_font,
    )

    draw.text(
        (tear_x + 80, ticket_y + 460),
        "1998",
        fill=INK_COLOR,
        font=main_font,
    )

    # Blood drop
    drop_x = tear_x
    drop_y = ticket_y + 360

    draw.polygon(
        [
            (drop_x, drop_y - 30),
            (drop_x - 12, drop_y),
            (drop_x + 12, drop_y),
        ],
        fill=BLOOD_COLOR,
    )

    draw.ellipse(
        [
            drop_x - 12,
            drop_y - 10,
            drop_x + 12,
            drop_y + 15,
        ],
        fill=BLOOD_COLOR,
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    img.save(output_path)

    print(f"Image created: {output_path}")


if __name__ == "__main__":
    create_ticket(
        output_path="output/cinema_ticket_vintage.png"
    )