# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Abkhas/news-image-20261124-entry/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Abkhas/news-image-20261124-entry/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

30-story dense family, Tuesday 24 November 2026. Three heroes with
drawn scenes (Nvidia brings Huang back, Ukraine sinks the Russian
corvette Merkury off Libya, COP31 collapses with no deal), 10 big
grid cards, 17 ALSO ON lines, a UTC timeline of Monday 23 November
(the day behind Tuesday's front page), a stat strip, a map with
numbered pins, a DATE CHECK strip, and a footer that says exactly
which days the stories come from. Every story is dated in its panel:
built at dawn in Asia, before the 24-November day had produced its
own news, so the heroes are the verified overnight stories of
22–23 November, honestly dated — never presented as 24-November
news.

- `main.py` — entry program; copies `entry.png` into the output
  folder and checks the copy's size. No drawing, no network, no
  randomness.
- `paint_n24.py` — draws the 1024x1024 image in code (PIL only),
  written fresh for this entry. Every scene is painted on its own
  layer and pasted in, so no scene can leak past its panel.
- `entry.png` — the rendered image (deterministic, two runs
  identical, 199,156 bytes).

SPDX-License-Identifier: MIT
