# Tuesday 24 November 2026 in One Picture

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Abkhas/news-image-20261124-entry/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Abkhas/news-image-20261124-entry/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One 1024×1024 newspaper page summing up the world news of **Tuesday 24 November 2026** — 35 stories, every one first reported that day (UTC).

## What's on the page

- **Masthead:** giant serif date, Tuesday kicker, red subhead naming the three leads.
- **Heroes:** Huawei convicted on 10 of 12 counts · four tankers hit by mines in the Strait of Hormuz · the PIF tower hit in Riyadh — each with a drawn scene, a status chip, and its UTC time.
- **Grid:** 10 more stories, each with a small pictogram — Nvidia gives back $240bn, Sudan shoots down drones from Ethiopia, Senegal win back AFCON, the Cartagena hostage siege, the WHO chief's Cuba visit, and five more.
- **The day in UTC:** a 10-beat timeline strip, 00:00 to 20:41.
- **Also on:** 22 further stories in three columns — including the Progress MS-36 cargo launch to the ISS, Australia's biggest battery plan, Ethiopia's Sudan peace offer, and Brazil's inflation outlook.
- **Date check:** six near-misses left out on purpose — including the Sparta II strike (Sat 21 Nov), the El Chapo Isidro capture (Fri 20 Nov) and the Merkury sinking off Libya (Sun 22 Nov), all of which made the news on Tuesday only as confirmations or follow-ups — plus a region bar showing where the 35 stories come from.

## How it was built

`paint_n24_v2.py` draws the page with PIL (DejaVu Serif + DejaVu Sans) and writes `entry.png`. `main.py` only copies the committed `entry.png` to the output directory — it never re-renders.

## Sources

Daily Summary Of "World News: 24 November 2026" (30 stories, 64 sources), cross-checked against Reuters, AP, Investopedia, Motley Fool, and Just Security — plus five stories from outside that pool, each first reported 24 Nov: NASA (Progress MS-36), RenewEconomy (Australia's biggest battery), MercoPress (Brazil's inflation outlook), ENA (Ethiopia's Sudan peace offer), and the COP31 backlash in Australia. Times in UTC; the mine claims in the Strait of Hormuz are flagged as unconfirmed (JMIC).

SPDX-License-Identifier: MIT
