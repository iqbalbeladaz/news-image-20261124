#!/usr/bin/env python3
"""Draw the whole of Tuesday 24 November 2026 on one square page.

Original renderer for the make.fun news-image-20261124 entry. It
paints a broadsheet front page with Pillow: a navy masthead carrying
the date, eight story cards in two columns, a dark "also today"
band of one-line briefs, and a closing line. All headlines were
gathered from the wires and roundups published on 24 November 2026
and cross-checked across at least two of them before being set.

Run:  python3 generate.py   ->   entry.png (1024 x 1024)
"""

import os

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
PAPER = (246, 241, 230)
CARD_BG = (255, 255, 255)
CARD_LINE = (208, 199, 178)
TEXT_DARK = (20, 20, 24)
TEXT_SOFT = (88, 86, 90)
BAND = (15, 23, 46)
BAND_TEXT = (238, 241, 248)
GOLD = (250, 205, 70)
RULE_RED = (226, 58, 44)

FONTS = "/usr/share/fonts/truetype/dejavu"


def font(bold, size):
    file = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONTS, file), size)


def wrap_px(draw, words, fnt, max_w):
    """Greedy word wrap measured in pixels, not characters."""
    lines, cur = [], ""
    for w in words.split():
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def shrink_to(draw, text, bold, start, max_w):
    size = start
    while size > 13 and draw.textlength(text, font=font(bold, size)) > max_w:
        size -= 1
    return font(bold, size)


def card(draw, x, y, w, h, colour, tag, head, body):
    """A story card: white box, coloured spine, tag, headline, body."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=12,
                           fill=CARD_BG, outline=CARD_LINE, width=2)
    draw.rounded_rectangle([x, y, x + 12, y + h], radius=6, fill=colour)
    tx = x + 28
    tw = w - 44
    draw.text((tx, y + 13), tag, font=font(True, 16), fill=colour)
    cy = y + 40
    for line in wrap_px(draw, head, font(True, 24), tw)[:2]:
        f = shrink_to(draw, line, True, 24, tw)
        draw.text((tx, cy), line, font=f, fill=TEXT_DARK)
        cy += 29
    cy += 2
    # Pick the largest body size whose wrapped lines still end
    # inside the card; a long body must never spill past the edge.
    size = 17
    while size > 12:
        lines = wrap_px(draw, body, font(False, size), tw)
        if cy + len(lines) * (size + 4) <= y + h - 8:
            break
        size -= 1
    for line in lines:
        draw.text((tx, cy), line, font=font(False, size), fill=TEXT_SOFT)
        cy += size + 4


def brief_band(draw, x, y, w, h, briefs):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=BAND)
    draw.text((x + 22, y + 13), "ALSO TODAY", font=font(True, 21), fill=GOLD)
    cy = y + 46
    for b in briefs:
        f = shrink_to(draw, "•  " + b, True, 16, w - 44)
        draw.text((x + 22, cy), "•  " + b, font=f, fill=BAND_TEXT)
        cy += 24


STORIES = [
    ((46, 92, 186), "SPACE — NATO",
     "NATO VOWS TO DEFEND SPACE",
     "Rutte pledges a response to any threat in space as reports "
     "say Russia may orbit a nuclear-armed satellite."),
    ((20, 132, 84), "WORLD COURT — THE HAGUE",
     "MYANMAR RULED ON GENOCIDE",
     "The World Court finds genocide against the Rohingya; "
     "fourteen countries publicly back the judgment."),
    ((206, 54, 40), "HEALTH — DR CONGO",
     "FIGHTING TRAPS EBOLA TEAMS",
     "Battle near an Ituri hospital forces Ebola responders "
     "under cover for more than a day, the WHO says."),
    ((178, 118, 18), "TECH — NVIDIA",
     "HUANG RETURNS TO NVIDIA",
     "Jensen Huang is restored as chief executive after Trump "
     "presses the board; markets surge worldwide."),
    ((126, 66, 168), "WAR — GAZA",
     "SIX KILLED IN GAZA STRIKES",
     "Israeli air strikes kill at least six Palestinians, among "
     "them a senior Hamas internal-security chief."),
    ((8, 128, 138), "SPACE — CHINA",
     "FIRST PAKISTANI FLIES TO TIANGONG",
     "Shenzhou-24 carries Muhammad Zeeshan Ali to China's "
     "station, its first foreign crew member."),
    ((64, 64, 160), "WAR — UKRAINE",
     "STRIKE KILLS 2, WOUNDS 48",
     "A Russian strike hits Ukraine as a new analysis counts "
     "more than 700,000 Russian war dead."),
    ((196, 96, 20), "DIPLOMACY — IRAN",
     "IRAN SETS SEVEN CONDITIONS",
     "Tehran rules out talks until Washington meets its terms; "
     "tankers strike mines in the Strait of Hormuz."),
]

BRIEFS = [
    "LIBYA — Ukrainian naval drones hit a Russian warship off Benghazi.",
    "MALAYSIA — Over 6,500 Rohingya refugees to be returned to Myanmar.",
    "USA — Measles elimination status lost after 25 years; ninth death in Pennsylvania.",
    "BUSINESS — Sanofi agrees a $41 billion takeover of US biotech Insmed.",
    "SCIENCE — A quasar shining 630 million years after the Big Bang, the earliest yet seen.",
]


def render():
    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead.
    d.rectangle([0, 0, PAGE, 140], fill=BAND)
    d.text((34, 16), "THE WORLD IN ONE DAY", font=font(True, 50),
           fill=(255, 255, 255))
    d.rectangle([34, 80, 990, 84], fill=RULE_RED)
    d.text((34, 94), "TUESDAY  24 NOVEMBER 2026", font=font(True, 32),
           fill=GOLD)
    d.text((990, 98), "ONE PAGE  •  THE WHOLE DAY",
           font=font(True, 18), fill=(205, 213, 232), anchor="ra")

    # Story grid: two columns, four rows.
    margin, gap_x, gap_y = 32, 16, 12
    cw = (PAGE - 2 * margin - gap_x) // 2
    ch = 146
    top = 152
    for i, (colour, tag, head, body) in enumerate(STORIES):
        x = margin + (i % 2) * (cw + gap_x)
        y = top + (i // 2) * (ch + gap_y)
        card(d, x, y, cw, ch, colour, tag, head, body)

    # Briefs and closing line.
    band_top = top + 4 * ch + 3 * gap_y + 14
    brief_band(d, margin, band_top, PAGE - 2 * margin, 168, BRIEFS)
    d.text((PAGE // 2, 972), "Eight stories, five briefs, one day — "
           "the world as Tuesday left it.",
           font=font(False, 18), fill=TEXT_SOFT, anchor="ma")

    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "entry.png")
    img.save(path, optimize=True)
    print("wrote", path, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    render()
