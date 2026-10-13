from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH = 900
HEIGHT = 650

BACKGROUND_COLOR = (192, 192, 192)
TITLE_BAR_COLOR = (0, 0, 128)
TEXT_COLOR = (0, 0, 0)
ACCENT_COLOR = (180, 0, 0)
LIGHT_BORDER = (255, 255, 255)
DARK_BORDER = (105, 105, 105)
MID_BORDER = (128, 128, 128)
BODY_COLOR = (255, 255, 255)


def load_font(primary_font, fallback_font, size):
    try:
        return ImageFont.truetype(primary_font, size)
    except OSError:
        try:
            return ImageFont.truetype(fallback_font, size)
        except OSError:
            return ImageFont.load_default()


def create_message_hoax(
    output_path="output/message_hoax.png",
):
    img = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        BACKGROUND_COLOR,
    )
    draw = ImageDraw.Draw(img)

    title_font = load_font(
        "arialbd.ttf",
        "DejaVuSans-Bold.ttf",
        22,
    )

    text_font = load_font(
        "cour.ttf",
        "DejaVuSansMono.ttf",
        24,
    )

    header_font = load_font(
        "arial.ttf",
        "DejaVuSans.ttf",
        20,
    )

    window_margin = 30

    draw.rectangle(
        [
            window_margin,
            window_margin,
            WIDTH - window_margin,
            HEIGHT - window_margin,
        ],
        fill=BACKGROUND_COLOR,
        outline=LIGHT_BORDER,
        width=3,
    )

    draw.line(
        [
            (WIDTH - window_margin, window_margin),
            (WIDTH - window_margin, HEIGHT - window_margin),
        ],
        fill=DARK_BORDER,
        width=3,
    )

    draw.line(
        [
            (window_margin, HEIGHT - window_margin),
            (WIDTH - window_margin, HEIGHT - window_margin),
        ],
        fill=DARK_BORDER,
        width=3,
    )

    title_bar_height = 35

    draw.rectangle(
        [
            window_margin + 3,
            window_margin + 3,
            WIDTH - window_margin - 3,
            window_margin + title_bar_height,
        ],
        fill=TITLE_BAR_COLOR,
    )

    draw.text(
        (window_margin + 12, window_margin + 6),
        "New Message",
        fill=LIGHT_BORDER,
        font=title_font,
    )

    header_start_y = window_margin + title_bar_height + 10

    draw.text(
        (window_margin + 15, header_start_y),
        "File  Edit  View  Insert  Format  Tools  Message  Help",
        fill=TEXT_COLOR,
        font=header_font,
    )

    draw.line(
        [
            (window_margin + 10, header_start_y + 30),
            (WIDTH - window_margin - 10, header_start_y + 30),
        ],
        fill=MID_BORDER,
        width=1,
    )

    draw.text(
        (window_margin + 15, header_start_y + 40),
        "To:       Everyone",
        fill=TEXT_COLOR,
        font=header_font,
    )

    draw.text(
        (window_margin + 15, header_start_y + 70),
        "Subject:",
        fill=TEXT_COLOR,
        font=header_font,
    )

    draw.text(
        (window_margin + 105, header_start_y + 70),
        "Warning — MUST READ",
        fill=ACCENT_COLOR,
        font=header_font,
    )

    draw.line(
        [
            (window_margin + 10, header_start_y + 105),
            (WIDTH - window_margin - 10, header_start_y + 105),
        ],
        fill=MID_BORDER,
        width=1,
    )

    body_margin = window_margin + 15
    body_start_y = header_start_y + 120

    draw.rectangle(
        [
            body_margin,
            body_start_y,
            WIDTH - body_margin,
            HEIGHT - body_margin - 15,
        ],
        fill=BODY_COLOR,
        outline=MID_BORDER,
        width=2,
    )

# Message text adapted from Bartlett (1999), The Austin Chronicle:
# https://www.austinchronicle.com/columns/about-aids-11732107/

    story_text = """Be careful the next time you go to a cinema.
These people could be anywhere!!

An experience of a friend of my brother's wife
left me speechless. Please send this to everyone
you know.

Some college girls went to see a movie. During
the show one of the girls felt a slight pinprick
sensation. Leaving the theater, her friend noticed
a sticker on the back of her dress reading:"""

    draw.text(
        (body_margin + 20, body_start_y + 20),
        story_text,
        fill=TEXT_COLOR,
        font=text_font,
    )

    punchline_text = """        "WELCOME TO THE REAL WORLD,
         YOU'RE HIV POSITIVE."""

    draw.text(
        (body_margin + 20, body_start_y + 300),
        punchline_text,
        fill=ACCENT_COLOR,
        font=text_font,
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    img.save(output_path)

    print(f"Image created: {output_path}")


if __name__ == "__main__":
    create_message_hoax()