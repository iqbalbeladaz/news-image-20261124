[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/iqbalbeladaz/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/iqbalbeladaz/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

# The World in One Day — Tuesday 24 November 2026

My entry for the make.fun bounty `news-image-20261124` ("Sum up
24 November's world news in one image", $100 pool). The whole of
Tuesday 24 November 2026, set as a single 1024×1024 broadsheet page.

## How it is put together

- `generate.py` — an original Pillow renderer. It paints the page
  from nothing: navy masthead with the date, eight story cards in
  two columns, a dark "also today" band of one-line briefs, and a
  closing line. Run it and it writes `entry.png`.
- `entry.png` — the finished picture, 1024×1024, regenerated
  byte-for-byte by the script above.
- `main.ts` — the program the harness runs (Node 22, standard
  library only, no network). It simply delivers the picture to
  `$MAKEFUN_OUTPUT_DIR/entry.png`, defaulting to `/output`.

## The day it covers

Eight lead stories, each first reported on Tuesday 24 November 2026:

1. NATO chief Mark Rutte vows the alliance will answer any threat
   in space, as reports circulate that Russia is preparing a
   nuclear-armed satellite.
2. The International Court of Justice finds that Myanmar committed
   genocide against the Rohingya; fourteen countries back the ruling.
3. Fighting near a hospital in Ituri, DR Congo traps Ebola response
   teams and forces them under cover for over 24 hours (WHO).
4. Jensen Huang returns as Nvidia's chief executive after Donald
   Trump intervenes with the board; markets surge.
5. Israeli air strikes on Gaza kill at least six Palestinians,
   including a senior Hamas internal-security commander.
6. China's Shenzhou-24 mission carries Pakistani astronaut Muhammad
   Zeeshan Ali to the Tiangong station — its first foreign crew member.
7. A Russian strike on Ukraine kills 2 and wounds 48, as a new
   analysis counts Russia's war dead above 700,000.
8. Iran rules out negotiations until Washington meets its seven
   conditions, while tankers strike mines in the Strait of Hormuz.

Briefs along the bottom: Ukrainian naval drones hit a Russian
warship off Benghazi; Malaysia prepares to return over 6,500
Rohingya refugees to Myanmar; the US loses measles elimination
status after 25 years, with a ninth death in Pennsylvania; Sanofi
agrees a $41 billion takeover of Insmed; and astronomers spot a
quasar shining just 630 million years after the Big Bang.

Every headline was cross-checked across at least two of the day's
sources (UN News, BBC, Reuters reporting, the Kyiv Independent, AP
copy and the 24 November roundups) before it was set on the page.

## License

MIT — see `LICENSE`.
