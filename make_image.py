#!/usr/bin/env python3
"""
The Daily Picture -- front page for Thursday 19 November 2026.

Draws a complete newspaper front page (1024 x 1024 PNG) with nothing but
Pillow primitives: rules, type, three flags over a summit table, and four
small spot illustrations.  No photographs, no randomness, no clock -- the
same code always produces the same bytes.

Stories (cross-checked 19 Nov 2026): the Trump-Xi-Putin trilateral at
APEC in Shenzhen, Anthropic's record IPO, Israeli tanks crossing Gaza's
Yellow Line, the GTA VI rollout, and the record Van Gogh sale, plus
three one-line minis and an "also today" footer.
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette
PAPER = (247, 242, 231)      # warm newsprint
PANEL = (239, 232, 213)      # slightly deeper cream for icon panels
INK = (26, 25, 23)           # near-black
SOFT = (96, 92, 84)          # grey-brown for the caption
RED = (156, 40, 38)          # kicker / accent red
NAVY = (33, 58, 95)          # secondary accent
GOLD = (172, 128, 44)        # rule gold
OLIVE = (94, 106, 70)        # tank green
OLIVE_DARK = (58, 66, 44)

SIZE = 1024
MARGIN = 46
RIGHT = SIZE - MARGIN
WIDTH = RIGHT - MARGIN

FONT_ROOT = "/usr/share/fonts/truetype"
FONT_FILES = {
    "serif": "dejavu/DejaVuSerif.ttf",
    "serif-bold": "dejavu/DejaVuSerif-Bold.ttf",
    "serif-italic": "liberation/LiberationSerif-Italic.ttf",
    "sans": "dejavu/DejaVuSans.ttf",
    "sans-bold": "dejavu/DejaVuSans-Bold.ttf",
}


def load_font(kind, size):
    return ImageFont.truetype(f"{FONT_ROOT}/{FONT_FILES[kind]}", size)


# ---------------------------------------------------------------- helpers
def text_w(draw, s, font):
    return draw.textlength(s, font=font)


def wrap_text(draw, s, font, max_w):
    """Greedy word wrap; returns a list of lines that each fit max_w."""
    lines, current = [], ""
    for word in s.split():
        trial = word if not current else current + " " + word
        if text_w(draw, trial, font) <= max_w or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def tracked_w(draw, s, font, tracking):
    return sum(text_w(draw, ch, font) for ch in s) + tracking * (len(s) - 1)


def draw_tracked(draw, x, y, s, font, fill, tracking):
    cx = x
    for ch in s:
        draw.text((cx, y), ch, font=font, fill=fill)
        cx += text_w(draw, ch, font) + tracking
    return cx - tracking


def centered(draw, cx, y, s, font, fill):
    draw.text((cx - text_w(draw, s, font) / 2, y), s, font=font, fill=fill)


def fit_size(draw, s, kind, start, max_w, floor=10):
    """Largest font size (<= start) whose rendering of s fits max_w."""
    size = start
    while size > floor and text_w(draw, s, load_font(kind, size)) > max_w:
        size -= 1
    return load_font(kind, size)


def star_points(cx, cy, r_out, r_in, rot_deg=-90):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot_deg + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def rule(draw, y, thick=1, fill=INK, x0=MARGIN, x1=RIGHT):
    draw.rectangle([x0, y, x1, y + thick - 1], fill=fill)


# ---------------------------------------------------------------- flags
def flag_usa(d, x, y, w, h):
    stripe = h / 13
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    for i in range(0, 13, 2):
        d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                    fill=(178, 34, 52))
    canton_w, canton_h = w * 0.42, stripe * 7
    d.rectangle([x, y, x + canton_w, y + canton_h], fill=(38, 52, 110))
    for row in range(4):
        for col in range(5):
            sx = x + 8 + col * (canton_w - 14) / 4
            sy = y + 7 + row * (canton_h - 12) / 3
            d.ellipse([sx - 2.4, sy - 2.4, sx + 2.4, sy + 2.4],
                      fill=(255, 255, 255))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def flag_china(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(204, 38, 30))
    d.polygon(star_points(x + w * 0.22, y + h * 0.30, 17, 6.8),
              fill=(250, 205, 40))
    for i, (dx, dy) in enumerate([(0.42, 0.14), (0.47, 0.32),
                                  (0.47, 0.52), (0.42, 0.68)]):
        rot = -90 + (i - 1.5) * 24
        d.polygon(star_points(x + w * dx, y + h * dy, 7, 2.8, rot),
                  fill=(250, 205, 40))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def flag_russia(d, x, y, w, h):
    band = h / 3
    d.rectangle([x, y, x + w, y + band], fill=(245, 245, 245))
    d.rectangle([x, y + band, x + w, y + 2 * band], fill=(36, 84, 160))
    d.rectangle([x, y + 2 * band, x + w, y + h], fill=(198, 40, 40))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def summit_table(d, top):
    """Three flags on poles behind one long table, nameplates in front."""
    flag_w, flag_h = 164, 92
    centers = [SIZE // 2 - 252, SIZE // 2, SIZE // 2 + 252]
    flags = [flag_usa, flag_china, flag_russia]
    names = ["TRUMP", "XI JINPING", "PUTIN"]
    table_y = top + flag_h + 24

    for cx, draw_flag in zip(centers, flags):
        draw_flag(d, cx - flag_w // 2, top, flag_w, flag_h)
        d.line([cx, top + flag_h, cx, table_y], fill=INK, width=3)

    # seated figures: a head and shoulders behind each nameplate
    for cx in centers:
        d.ellipse([cx - 11, table_y - 34, cx + 11, table_y - 12], fill=INK)
        d.pieslice([cx - 21, table_y - 24, cx + 21, table_y + 14],
                   start=180, end=360, fill=INK)

    d.rectangle([MARGIN + 40, table_y, RIGHT - 40, table_y + 15], fill=NAVY)

    plate_font = load_font("sans-bold", 15)
    for cx, name in zip(centers, names):
        pw = text_w(d, name, plate_font) + 22
        d.rectangle([cx - pw / 2, table_y - 3, cx + pw / 2, table_y + 19],
                    fill=PAPER, outline=INK, width=2)
        centered(d, cx, table_y + 1, name, plate_font, INK)
    return table_y + 15


# ---------------------------------------------------------------- icons
def icon_panel(d, x, y, s=96):
    d.rectangle([x, y, x + s, y + s], fill=PANEL, outline=INK, width=2)


def icon_chart(d, x, y):
    icon_panel(d, x, y)
    d.line([x + 14, y + 14, x + 14, y + 80], fill=INK, width=3)
    d.line([x + 14, y + 80, x + 84, y + 80], fill=INK, width=3)
    for i, (bh, col) in enumerate([(22, NAVY), (36, GOLD), (52, RED)]):
        bx = x + 24 + i * 19
        d.rectangle([bx, y + 80 - bh, bx + 12, y + 80], fill=col)
    pts = [(x + 20, y + 60), (x + 39, y + 45), (x + 57, y + 35),
           (x + 79, y + 17)]
    d.line(pts, fill=RED, width=4)
    d.polygon([(x + 79, y + 17), (x + 68, y + 18), (x + 77, y + 27)],
              fill=RED)


def icon_tank(d, x, y):
    icon_panel(d, x, y)
    d.line([x + 60, y + 36, x + 90, y + 31], fill=OLIVE_DARK, width=6)
    d.rectangle([x + 34, y + 33, x + 62, y + 48], fill=OLIVE)
    d.polygon([(x + 15, y + 63), (x + 81, y + 63), (x + 71, y + 48),
               (x + 25, y + 48)], fill=OLIVE)
    d.rounded_rectangle([x + 9, y + 62, x + 87, y + 81], radius=9,
                        fill=OLIVE_DARK)
    for i in range(4):
        wx = x + 24 + i * 16
        d.ellipse([wx - 5, y + 66, wx + 5, y + 76], fill=(30, 34, 24))


def icon_controller(d, x, y):
    icon_panel(d, x, y)
    d.ellipse([x + 6, y + 52, x + 28, y + 74], fill=(36, 36, 42))
    d.ellipse([x + 68, y + 52, x + 90, y + 74], fill=(36, 36, 42))
    d.rounded_rectangle([x + 8, y + 28, x + 88, y + 64], radius=12,
                        fill=(36, 36, 42))
    d.rectangle([x + 25, y + 38, x + 35, y + 56], fill=(214, 208, 196))
    d.rectangle([x + 20, y + 43, x + 40, y + 51], fill=(214, 208, 196))
    d.ellipse([x + 63, y + 36, x + 73, y + 46], fill=RED)
    d.ellipse([x + 73, y + 48, x + 83, y + 58], fill=GOLD)
    d.rectangle([x + 44, y + 46, x + 54, y + 51], fill=(150, 148, 140))


def icon_painting(d, x, y):
    icon_panel(d, x, y)
    d.rectangle([x + 13, y + 9, x + 83, y + 87], fill=GOLD)
    d.rectangle([x + 19, y + 15, x + 77, y + 81], fill=(30, 42, 74))
    d.rectangle([x + 19, y + 72, x + 77, y + 81], fill=(86, 120, 70))
    brown = (112, 76, 46)
    d.line([x + 48, y + 74, x + 48, y + 56], fill=brown, width=4)
    d.line([x + 48, y + 60, x + 39, y + 48], fill=brown, width=3)
    d.line([x + 48, y + 58, x + 57, y + 46], fill=brown, width=3)
    pink = (233, 158, 178)
    for cx, cy, r in [(38, 36, 8), (48, 29, 9), (59, 36, 8),
                      (42, 45, 7), (55, 45, 7), (48, 39, 7)]:
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                  fill=pink)
    d.polygon(star_points(x + 67, y + 25, 6, 2.4), fill=(250, 205, 40))


# ---------------------------------------------------------------- blocks
def story_cell(d, x, y, icon, headline, body):
    icon(d, x, y)
    tx = x + 112
    tw = x + 466 - tx
    head_font = load_font("sans-bold", 23)
    body_font = load_font("sans", 18)
    cy = y
    for line in wrap_text(d, headline, head_font, tw):
        d.text((tx, cy), line, font=head_font, fill=INK)
        cy += 27
    cy += 3
    for line in wrap_text(d, body, body_font, tw):
        d.text((tx, cy), line, font=body_font, fill=INK)
        cy += 22
    return cy


def mini_column(d, x, y, w, place, body):
    d.text((x, y), place, font=load_font("sans-bold", 19), fill=RED)
    body_font = load_font("sans", 17)
    cy = y + 25
    for line in wrap_text(d, body, body_font, w):
        d.text((x, cy), line, font=body_font, fill=INK)
        cy += 22
    return cy


# ---------------------------------------------------------------- page
def build_page():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)

    # hairline frame
    d.rectangle([16, 16, SIZE - 17, SIZE - 17], outline=INK, width=1)
    d.rectangle([20, 20, SIZE - 21, SIZE - 21], outline=INK, width=1)

    # masthead
    mast = fit_size(d, "THE DAILY PICTURE", "serif-bold", 60, WIDTH)
    centered(d, SIZE // 2, 30, "THE DAILY PICTURE", mast, INK)
    rule(d, 104, thick=3, fill=GOLD)
    rule(d, 111, thick=1)

    # dateline row
    line_font = load_font("sans-bold", 21)
    d.text((MARGIN, 120), "Thursday 19 November 2026",
           font=line_font, fill=INK)
    tag = "THE WHOLE WORLD'S NEWS, IN ONE IMAGE"
    d.text((RIGHT - text_w(d, tag, line_font), 120), tag,
           font=line_font, fill=NAVY)
    rule(d, 149, thick=4)
    rule(d, 156, thick=1)

    # lead story
    kicker_font = load_font("sans-bold", 22)
    draw_tracked(d, MARGIN, 170, "LEAD STORY — APEC SUMMIT · SHENZHEN, CHINA",
                 kicker_font, RED, 1.5)
    head_font = load_font("serif-bold", 48)
    y = 198
    for line in wrap_text(d, "Trump, Xi & Putin Meet at One Table in Shenzhen",
                          head_font, WIDTH):
        d.text((MARGIN, y), line, font=head_font, fill=INK)
        y += 56
    deck_font = load_font("serif", 22)
    for line in wrap_text(
            d,
            "The U.S., Chinese and Russian presidents meet face to face for "
            "the first time — nuclear arms, Ukraine, Iran and trade on the "
            "agenda.",
            deck_font, WIDTH):
        d.text((MARGIN, y + 2), line, font=deck_font, fill=INK)
        y += 28

    table_bottom = summit_table(d, y + 14)
    cap_font = load_font("serif-italic", 20)
    centered(d, SIZE // 2, table_bottom + 10,
             "Three flags, one table — the first trilateral summit, held "
             "on APEC's sidelines.", cap_font, SOFT)
    rule(d, table_bottom + 40, thick=2)

    # four stories in a two-by-two grid
    grid_y = table_bottom + 52
    story_cell(d, MARGIN, grid_y, icon_chart,
               "ANTHROPIC'S $81.3B IPO IS THE BIGGEST EVER",
               "Claude's maker priced shares at $83 — a near $1.5 trillion "
               "value. Trading starts today on Nasdaq.")
    story_cell(d, SIZE // 2 + 14, grid_y, icon_tank,
               "ISRAELI TANKS CROSS GAZA'S YELLOW LINE",
               "First ground push past the truce line since Oct. 2025, "
               "near Nuseirat and Bureij; Hamas cries breach.")
    grid2_y = grid_y + 135
    story_cell(d, MARGIN, grid2_y, icon_controller,
               "GTA VI FINALLY ARRIVES WORLDWIDE",
               "After a 13-year wait, gamers flood back into Vice City "
               "as the rollout begins worldwide.")
    story_cell(d, SIZE // 2 + 14, grid2_y, icon_painting,
               "VAN GOGH SELLS FOR A RECORD $190.4M",
               "'Blossoming Chestnut Trees' (1890) tops his old record; "
               "a Nazi-era claim was settled.")
    rule(d, grid2_y + 131, thick=1)

    # three one-line minis
    mini_y = grid2_y + 143
    col_w, gap = 298, 19
    mini_column(d, MARGIN, mini_y, col_w, "BRUSSELS",
                "EU proposes a €45B Ukraine loan, repaid once Russia "
                "pays reparations.")
    mini_column(d, MARGIN + col_w + gap, mini_y, col_w, "WASHINGTON",
                "Democrats pick Jeffries as Speaker-designate — first "
                "Black Speaker in line.")
    mini_column(d, MARGIN + 2 * (col_w + gap), mini_y, col_w, "THE GULF",
                "U.S. sends a third carrier to the Gulf as Iran clashes "
                "widen at Hormuz.")

    # footer
    rule(d, 950, thick=1)
    foot = ("ALSO TODAY — Cyclone Akvan nears India · Estonia to close "
            "its Russia border in December · France protests")
    foot_font = fit_size(d, foot, "sans-bold", 17, WIDTH, floor=12)
    centered(d, SIZE // 2, 960, foot, foot_font, NAVY)

    return img


def main():
    out = Path(__file__).resolve().parent / "entry.png"
    build_page().save(out, format="PNG")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
