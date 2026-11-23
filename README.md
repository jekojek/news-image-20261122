# The World in One Day — 22 November 2026

[![make.fun competition](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/c/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/jekojek/news-image-20261122/rank.svg)](https://make.fun/c/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/jekojek/news-image-20261122/reward.svg)](https://make.fun/c/news-image-20261122)

A one-page newspaper front page that sums up the world's news of
**Sunday 22 November 2026**, drawn from scratch with Pillow.

## The day in the paper

- **Lead story — climate summit collapses:** COP31 ends with no deal as talks
  fail on fossil fuels. The EU and others reject a text with no mention of
  fossil fuels, and the Antalya summit closes two days late with no agreement
  from nearly 200 countries.
- **War at sea:** Ukrainian sea drones strike a Russian warship — the corvette
  Merkury is badly damaged at Benghazi, Libya, and a cargo ship is also hit.
- **War in Europe:** a Russian strike flattens a Kyiv apartment block in
  Dymer, near Kyiv; at least 3 killed, people trapped under the rubble.
- **Politics:** Democrats win 258 House seats — the largest US House majority
  for any party since 1992.
- **Space:** BepiColombo reaches Mercury after 8 years; the ESA-JAXA probe
  enters orbit after a thruster glitch, the craft safe.
- **Justice:** Mexico captures "El Chapo Isidro" — FBI Most Wanted cartel boss
  Fausto Isidro Meza Flores seized in Sinaloa; 11 killed in the raid.
- **Disaster:** a candy factory fire kills 3 in Indonesia — a blaze at
  Cikande, Banten, with dozens of workers still missing.
- **Also:** Nigeria boat sinks, 24 dead — Iran hits 3 tankers near Hormuz.

## How it works

`main.ts` (Node 22, standard library only) runs `draw_news.py`, which draws
the whole 1024×1024 page with Pillow — masthead, lead story with a
no-deal globe, six illustrated stories in a two-column grid, and the footer —
and writes it to `entry.png` in the output directory. No network, no fonts
beyond the system Liberation set, and the output is byte-identical on
every run.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Entry

This repository is an entry in the
[make.fun competition "Sum up 22 November's world news in one image"](https://make.fun/c/news-image-20261122)
(`news-image-20261122`).

## License

MIT — see [LICENSE](LICENSE).
