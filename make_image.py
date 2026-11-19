#!/usr/bin/env python3
"""Draw the entry image for make.fun bounty news-image-20261119.

"The Daily Picture" — a newspaper front page that sums up the world news
of Thursday 19 November 2026 in one 1024x1024 frame, drawn entirely with
Pillow (no photographs), so a judge with no news feed can read the whole
day from the picture alone. Today's palette: "Amber Slate" — warm ivory
paper, deep slate ink, teal rules and amber kickers.

Stories cross-checked 19 Nov 2026 against several independent sources
(New York Times, Le Monde, Reuters, CNN, BBC, AFP, WSJ): Trump, Xi and
Putin hold a first trilateral summit at APEC in Shenzhen; Anthropic's
$81.3B IPO is the biggest stock-market debut ever and starts trading
today; Israeli tanks cross Gaza's Yellow Line for the first time since
the October 2025 ceasefire; Grand Theft Auto VI begins its global
rollout; a Van Gogh sells for a record $190.4M after a Nazi-era claim
is settled; the EU proposes a 45 billion euro loan for Ukraine;
Democrats pick Hakeem Jeffries as Speaker-designate; the U.S. sends a
third aircraft carrier toward the Middle East.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W = 1024
PAPER = (250, 246, 236)
INK = (24, 30, 38)
TEAL = (0, 102, 110)
AMBER = (196, 116, 16)
GREY = (100, 96, 88)
WHITE = (252, 252, 250)
PINK = (232, 160, 175)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, width):
    """Greedy word wrap measured in pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(draw, y, text, font, fill=INK):
    x = (W - draw.textlength(text, font=font)) / 2
    draw.text((x, y), text, font=font, fill=fill)


def star(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


img = Image.new("RGB", (W, W), PAPER)
d = ImageDraw.Draw(img)
M = 38
RIGHT = W - M

# ---------------------------------------------------------------- masthead
d.rectangle([M, 20, RIGHT, 25], fill=AMBER)
d.line([M, 33, RIGHT, 33], fill=INK, width=2)
centered(d, 46, "THE DAILY PICTURE", f(SERIF_B, 74))
centered(
    d,
    132,
    "Thursday 19 November 2026  ·  The whole world's news, in one image",
    f(SANS_B, 24),
    fill=TEAL,
)
d.line([M, 168, RIGHT, 168], fill=INK, width=3)
d.line([M, 173, RIGHT, 173], fill=INK, width=1)

# ---------------------------------------------------------------- lead story
d.text((M, 188), "LEAD STORY — APEC SUMMIT · SHENZHEN, CHINA", font=f(SANS_B, 23), fill=AMBER)
d.text((M, 222), "TRUMP, XI & PUTIN", font=f(SERIF_B, 50), fill=INK)
d.text((M, 286), "AT ONE TABLE IN SHENZHEN", font=f(SERIF_B, 50), fill=INK)
STAND = (
    "The U.S., Chinese and Russian presidents meet face to face for the "
    "first time — nuclear arms, Ukraine, Iran and trade on the agenda."
)
sy = 356
for line in wrap(d, STAND, f(SANS, 22), RIGHT - M):
    d.text((M, sy), line, font=f(SANS, 22), fill=INK)
    sy += 29

# ------------------------------------------------------- lead illustration
# The flags of the United States, China and Russia above one summit table.
def flag_usa(x, y):
    for i in range(7):
        col = (178, 34, 52) if i % 2 == 0 else WHITE
        d.rectangle([x, y + i * 10, x + 118, y + i * 10 + 10], fill=col)
    d.rectangle([x, y + 70, x + 118, y + 72], fill=WHITE)
    d.rectangle([x, y, x + 52, y + 40], fill=(60, 59, 110))
    for r in range(4):
        for c in range(5):
            d.ellipse([x + 5 + c * 10, y + 4 + r * 9, x + 9 + c * 10, y + 8 + r * 9], fill=WHITE)


def flag_china(x, y):
    d.rectangle([x, y, x + 118, y + 72], fill=(222, 41, 16))
    star(d, x + 30, y + 24, 15, (255, 222, 0))
    for dx, dy in [(52, 10), (58, 26), (58, 42), (50, 54)]:
        star(d, x + dx, y + dy, 5, (255, 222, 0))


def flag_russia(x, y):
    d.rectangle([x, y, x + 118, y + 24], fill=WHITE)
    d.rectangle([x, y + 24, x + 118, y + 48], fill=(0, 57, 166))
    d.rectangle([x, y + 48, x + 118, y + 72], fill=(213, 43, 30))


BAND_Y = 420
for fx, draw_flag in [(168, flag_usa), (453, flag_china), (738, flag_russia)]:
    d.rectangle([fx + 55, BAND_Y, fx + 60, BAND_Y + 84], fill=INK)  # pole
    draw_flag(fx, BAND_Y)
d.rectangle([128, BAND_Y + 84, 896, BAND_Y + 98], fill=TEAL)  # table slab
for cx in (256, 512, 768):  # microphones and place cards on the table
    d.line([cx, BAND_Y + 84, cx - 14, BAND_Y + 62], fill=INK, width=4)
    d.ellipse([cx - 22, BAND_Y + 54, cx - 6, BAND_Y + 66], fill=INK)
    d.rectangle([cx - 34, BAND_Y + 66, cx + 34, BAND_Y + 82], fill=WHITE, outline=INK, width=2)
centered(
    d,
    BAND_Y + 108,
    "Three flags, one table — a first trilateral summit on APEC's sidelines.",
    f(SANS, 19),
    fill=GREY,
)
d.line([M, 560, RIGHT, 560], fill=INK, width=2)

# ------------------------------------------------------------------- icons
def icon_chart(x, y):
    d.line([x + 8, y + 6, x + 8, y + 68], fill=INK, width=4)
    d.line([x + 8, y + 68, x + 104, y + 68], fill=INK, width=4)
    for i, h in enumerate((18, 30, 24, 44)):
        bx = x + 20 + i * 20
        d.rectangle([bx, y + 68 - h, bx + 13, y + 68], fill=TEAL)
    pts = [(x + 16, y + 48), (x + 44, y + 34), (x + 66, y + 40), (x + 96, y + 12)]
    d.line(pts, fill=AMBER, width=5)
    d.polygon([(x + 96, y + 12), (x + 82, y + 14), (x + 94, y + 26)], fill=AMBER)


def icon_tank(x, y):
    d.polygon([(x + 6, y + 44), (x + 20, y + 30), (x + 88, y + 30), (x + 102, y + 44),
               (x + 96, y + 62), (x + 12, y + 62)], fill=(84, 92, 60))
    d.rectangle([x + 34, y + 16, x + 66, y + 32], fill=(84, 92, 60))
    d.line([x + 62, y + 22, x + 110, y + 16], fill=INK, width=6)
    for i in range(5):
        cx = x + 22 + i * 16
        d.ellipse([cx - 7, y + 48, cx + 7, y + 62], fill=INK)
    d.line([x, y + 72, x + 110, y + 72], fill=GREY, width=3)


def icon_gamepad(x, y):
    d.rounded_rectangle([x + 4, y + 14, x + 106, y + 62], radius=22, fill=INK)
    d.rectangle([x + 24, y + 30, x + 34, y + 46], fill=WHITE)
    d.rectangle([x + 19, y + 35, x + 39, y + 41], fill=WHITE)
    for bx, by, col in [(82, 28, AMBER), (94, 40, TEAL), (70, 40, (178, 34, 52))]:
        d.ellipse([bx, by, bx + 10, by + 10], fill=col)


def icon_painting(x, y):
    d.rectangle([x + 6, y, x + 104, y + 74], fill=(168, 124, 44))
    d.rectangle([x + 14, y + 8, x + 96, y + 66], fill=(38, 54, 92))
    d.line([x + 55, y + 66, x + 55, y + 34], fill=(110, 74, 40), width=5)
    d.line([x + 55, y + 44, x + 40, y + 30], fill=(110, 74, 40), width=4)
    d.line([x + 55, y + 40, x + 70, y + 28], fill=(110, 74, 40), width=4)
    for cx, cy, r in [(38, 26, 11), (56, 18, 13), (74, 26, 11), (46, 34, 9), (66, 36, 9)]:
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r], fill=PINK)
    star(d, x + 88, y + 56, 8, (255, 222, 0))


def story(x, y, w, icon, headline, body):
    icon(x, y + 2)
    tx = x + 124
    hy = y
    for line in wrap(d, headline, f(SANS_B, 23), w - 124):
        d.text((tx, hy), line, font=f(SANS_B, 23), fill=INK)
        hy += 29
    by = hy + 3
    for line in wrap(d, body, f(SANS, 19), w - 124):
        d.text((tx, by), line, font=f(SANS, 19), fill=INK)
        by += 25


COL_W = 452
story(
    M, 578, COL_W, icon_chart,
    "ANTHROPIC'S $81.3B IPO IS THE BIGGEST EVER",
    "Claude's maker priced shares at $83, valuing it near $1.5 "
    "trillion; trading starts today on Nasdaq.",
)
story(
    M + COL_W + 44, 578, COL_W, icon_tank,
    "ISRAELI TANKS CROSS GAZA'S YELLOW LINE",
    "First push past the ceasefire line since the Oct. 2025 "
    "truce; Hamas cries breach.",
)
story(
    M, 726, COL_W, icon_gamepad,
    "GTA VI FINALLY ARRIVES WORLDWIDE",
    "After a 13-year wait, gamers flood back into Vice City as "
    "the global rollout begins.",
)
story(
    M + COL_W + 44, 726, COL_W, icon_painting,
    "VAN GOGH SELLS FOR A RECORD $190.4M",
    "'Blossoming Chestnut Trees' (1890) tops his record; "
    "Nazi-era claim settled.",
)
d.line([M, 876, RIGHT, 876], fill=INK, width=2)

# ------------------------------------------------------------- dateline minis
def mini(x, w, place, body):
    d.text((x, 890), place, font=f(SANS_B, 20), fill=AMBER)
    by = 918
    for line in wrap(d, body, f(SANS, 18), w):
        d.text((x, by), line, font=f(SANS, 18), fill=INK)
        by += 23


mini(M, 292, "BRUSSELS", "EU proposes €45B Ukraine loan, repaid from reparations.")
mini(M + 330, 292, "WASHINGTON", "Democrats pick Jeffries, first Black Speaker in line.")
mini(M + 660, 288, "THE GULF", "U.S. sends a third carrier as Iran clashes widen at Hormuz.")

# ------------------------------------------------------------------- footer
d.line([M, 972, RIGHT, 972], fill=INK, width=3)
centered(
    d,
    982,
    "ALSO TODAY — Cyclone Akvan nears India's coast · Estonia to shut Russia border · France protests",
    f(SANS_B, 17),
    fill=TEAL,
)

img.save("entry.png", optimize=True)
print("wrote entry.png", img.size)
