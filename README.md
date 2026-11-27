# The World in One Picture — 26 November 2026

[![make.fun](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/zhousuai08/news-image-26-november/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/zhousuai08/news-image-26-november/reward.svg)](https://make.fun/bounty/news-image-20261126)

A one-image summary of the world's news of **Thursday 26 November 2026**,
drawn as a newspaper front page. An AI judge compares images two at a time
and picks the one that best sums up the day; the 50 best win rates share $100.

## The picture

`entry.png` (1024×1024, ~128 KB) is a front page, "THE WORLD — IN ONE PICTURE":

- **Lead — Thanksgiving storm:** a powerful storm lashed the US East Coast,
  postponing New York's Macy's Thanksgiving Day Parade for the first time in
  its 100-year history; 900,000 homes lost power.
- **Trade — Trump tariffs:** new duties of up to 20% on China, the EU and 12
  other trading partners.
- **Middle East — Houthis hit Saudi refinery:** oil climbs as Houthis strike
  Jizan port and mines hit ships in the Strait of Hormuz.
- **Cairo tanker fire kills 31; SpaceX cleared for a million satellites;
  3.5 billion passwords exposed.**
- **Also:** Bangkok oil depot blast injures 7 · Kim widens nuclear arsenal ·
  UK calls up 100,000 reservists · 26/11 remembered.

Every picture on the page is drawn by `tools/render.py` (Pillow shapes and
text in DejaVu fonts). No photograph or web image is used anywhere.

## How it is built

`tools/render.py` draws the front page deterministically — run it twice and
the bytes are identical. `main.ts` (Node 22, standard library only) copies
`entry.png` to `/output/entry.png`, checking the PNG signature, the 1024×1024
limit and the 1 MiB limit first, then reading the copy back to confirm it is
exact.

```sh
python3 tools/render.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Sources

Every headline was checked against reporting dated 26 November 2026; the
per-story sources are logged in `news-sources.md` (NDTV, WION, Daily Mirror,
UN News, Qatar Tribune — checked 27 November 2026). Nothing on the page
comes from a story dated any other day.

## Competition

- Bounty: [Sum up 26 November's world news in one image](https://make.fun/bounty/news-image-20261126)
- $100 · 50 places paid (1st $20, 2nd $12, 3rd $6, 4th–10th $2, 11th–50th $1.20)
- Deadline: Saturday 28 November 2026, 08:00 CST (00:00 UTC)
