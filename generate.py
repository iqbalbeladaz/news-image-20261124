#!/usr/bin/env python3
"""Render the one-image summary of Tuesday 24 November 2026.

The picture is drawn from scratch with Pillow: a newspaper-style
masthead naming the day, six story panels (NATO and space, the ICJ
Rohingya ruling, Congo's Ebola responders, Nvidia, Gaza, Shenzhou-24)
and an "also today" strip with five shorter items. Every headline
below was checked against the day's wires and news roundups of
24 November 2026 before drawing.

Usage: python3 generate.py  (writes entry.png next to this file)
"""
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

CANVAS = 1024
CREAM = (247, 243, 232)
INK = (18, 18, 20)
CARD = (255, 255, 255)
GREY = (84, 84, 88)
NAVY = (16, 24, 48)
GOLD = (255, 209, 64)
RED = (232, 64, 52)
EDGE = (215, 208, 190)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(bold, size):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def fit_text(draw, text, bold, size, limit):
    """Largest size at or below `size` that fits `limit` pixels wide."""
    while size > 16:
        font = load_font(bold, size)
        if draw.textlength(text, font=font) <= limit:
            return font
        size -= 1
    return load_font(bold, size)


def story_panel(draw, box, accent, kicker, headline, body):
    """One white card: coloured top bar, kicker, headline, body copy."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=14, fill=CARD, outline=EDGE, width=2)
    draw.rectangle([x0, y0, x1, y0 + 10], fill=accent)
    draw.text((x0 + 20, y0 + 24), kicker, font=load_font(True, 17), fill=accent)
    cursor = y0 + 52
    for line in textwrap.wrap(headline, width=24):
        font = fit_text(draw, line, True, 27, (x1 - x0) - 40)
        draw.text((x0 + 20, cursor), line, font=font, fill=INK)
        cursor += 32
    cursor += 4
    lines = textwrap.wrap(body, width=39)
    size = 19
    # Shrink the body copy if it would run past the card's bottom edge.
    while size > 14 and cursor + len(lines) * (size + 5) > y1 - 10:
        size -= 1
    for line in lines:
        draw.text((x0 + 20, cursor), line, font=load_font(False, size), fill=GREY)
        cursor += size + 5


def brief_strip(draw, box, items):
    """Dark strip listing the shorter stories of the day."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=14, fill=NAVY)
    draw.text((x0 + 20, y0 + 14), "ALSO TODAY", font=load_font(True, 22), fill=GOLD)
    cursor = y0 + 50
    for item in items:
        text = "•  " + item
        font = fit_text(draw, text, True, 17, (x1 - x0) - 40)
        draw.text((x0 + 20, cursor), text, font=font, fill=(240, 243, 250))
        cursor += 27


def main():
    img = Image.new("RGB", (CANVAS, CANVAS), CREAM)
    draw = ImageDraw.Draw(img)

    # Masthead: paper name, red rule, the date in gold.
    draw.rectangle([0, 0, CANVAS, 150], fill=NAVY)
    draw.text((36, 18), "THE WORLD IN ONE DAY",
              font=load_font(True, 52), fill=(255, 255, 255))
    draw.rectangle([36, 86, 988, 90], fill=RED)
    draw.text((36, 100), "TUESDAY  24 NOVEMBER 2026",
              font=load_font(True, 34), fill=GOLD)
    draw.text((988, 100), "ONE IMAGE  •  THE DAY'S NEWS",
              font=load_font(True, 20), fill=(210, 218, 235), anchor="ra")

    stories = [
        dict(accent=(52, 92, 180), kicker="SPACE  •  NATO / RUSSIA",
             headline="NATO VOWS SPACE DEFENCE",
             body="Rutte says the alliance will defend against any "
                  "threat in space, amid reports Russia is preparing "
                  "a nuclear-armed satellite."),
        dict(accent=(22, 138, 90), kicker="WORLD COURT  •  THE HAGUE",
             headline="ICJ: GENOCIDE OF THE ROHINGYA",
             body="The World Court finds Myanmar committed genocide "
                  "against the Rohingya; 14 countries back the ruling."),
        dict(accent=(200, 52, 40), kicker="HEALTH  •  ITURI, DR CONGO",
             headline="EBOLA TEAMS TRAPPED",
             body="Heavy fighting near a hospital in Ituri traps Ebola "
                  "responders, forcing emergency teams to take cover "
                  "for over 24 hours (WHO)."),
        dict(accent=(176, 120, 20), kicker="TECH  •  NVIDIA, USA",
             headline="HUANG BACK AS NVIDIA CEO",
             body="Jensen Huang is reinstated as chief executive after "
                  "Trump intervenes with the board; markets surge."),
        dict(accent=(128, 70, 170), kicker="MIDDLE EAST  •  GAZA",
             headline="AIRSTRIKES KILL SIX IN GAZA",
             body="Israeli airstrikes kill at least six Palestinians, "
                  "including a senior Hamas security chief, medics say."),
        dict(accent=(10, 130, 140), kicker="SPACE  •  CHINA / PAKISTAN",
             headline="SHENZHOU-24 LIFTS OFF",
             body="China launches Shenzhou-24: a Pakistani astronaut "
                  "flies to the Tiangong station, its first foreign "
                  "crew member."),
    ]

    margin, gap = 36, 20
    width = (CANVAS - 2 * margin - gap) // 2
    height = 178
    top = 172
    for i, story in enumerate(stories):
        x = margin + (i % 2) * (width + gap)
        y = top + (i // 2) * (height + gap)
        story_panel(draw, (x, y, x + width, y + height), **story)

    briefs = [
        "UKRAINE: Russian strike kills 2 and wounds 48; analysis puts Russia's war dead above 700,000.",
        "IRAN: No talks until Washington meets seven conditions; tankers hit mines in the Strait of Hormuz.",
        "LIBYA: Ukrainian naval drones strike a Russian warship off Benghazi.",
        "MALAYSIA: Kuala Lumpur to return more than 6,500 Rohingya refugees to Myanmar.",
        "UNITED STATES: Measles elimination status lost after 25 years; a ninth death in Pennsylvania.",
    ]
    strip_top = top + 3 * (height + gap) + 2
    brief_strip(draw, (margin, strip_top, CANVAS - margin, 962), briefs)

    draw.text((CANVAS // 2, 982),
              "The day's biggest stories, across every region - in a single picture.",
              font=load_font(False, 18), fill=GREY, anchor="ma")

    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
