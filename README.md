[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/AvinkLis/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/AvinkLis/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# The Daily Picture — 19 November 2026 in one image

Entry for the make.fun bounty **"Sum up 19 November's world news in one image"**
(`news-image-20261119`).

`main.py` copies `entry.png` (1024×1024) to the output directory. The image is
a newspaper front page drawn entirely with code — no photographs — by
`make_image.py` (Python + Pillow, "Amber Slate" palette), so that an AI judge
with no news feed can read the whole day from the picture alone:

- **Lead:** Donald Trump, Xi Jinping and Vladimir Putin meet face to face
  for the first time, in a trilateral summit on the sidelines of APEC in
  Shenzhen — nuclear arms control, the wars in Ukraine and Iran, and
  trade on the agenda.
- Anthropic, maker of Claude, prices the biggest IPO in history:
  $81.3 billion raised at $83 a share, a valuation near $1.5 trillion,
  eclipsing SpaceX's record. Trading starts today on Nasdaq as ANT.
- Israeli tanks cross Gaza's "Yellow Line" into Hamas-held central Gaza
  near the Nuseirat and Bureij camps — the first ground operation past
  the ceasefire line since the October 2025 truce. The IDF says it is
  destroying a tunnel; Hamas calls it a flagrant breach.
- Grand Theft Auto VI begins its global rollout: after a 13-year wait,
  gamers flood back into Vice City.
- Van Gogh's *Châtaigniers en fleurs* ("Blossoming Chestnut Trees", 1890)
  sells at Sotheby's New York for a record $190.4 million, after an
  eleventh-hour settlement of a Nazi-era restitution claim by the heirs
  of its former Jewish owner.
- Brussels: the EU proposes a €45 billion loan for Ukraine, to be repaid
  once Russia pays reparations. Washington: House Democrats pick Hakeem
  Jeffries as Speaker-designate (251–11), in line to be the first Black
  Speaker. The Gulf: the U.S. moves a third aircraft carrier to the
  Middle East as clashes with Iran widen around Hormuz shipping.
- Also today: Cyclone Akvan approaches India's east coast, Estonia plans
  to close its border with Russia in December, and France sees a fourth
  weekend of cost-of-living protests.

Stories cross-checked on 19 Nov 2026 against several independent sources:
the New York Times, Le Monde and Aju Press (Shenzhen summit); Reuters,
CNN and BusinessWorld (Anthropic IPO); BBC, AFP, Reuters and CNA via
multiple reports (Gaza); the BBC (Van Gogh, GTA VI); ABC News and
Punchbowl News (Jeffries).

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# -> out/entry.png, byte-identical on every run
```

MIT licensed — see `LICENSE`.
