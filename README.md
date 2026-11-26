# news-image-20261126 v2 — The World in One Page

![news-image-20261126](https://make.fun/badge/news-image-20261126.svg)
![rank](https://make.fun/badge/news-image-20261126/Hoppererin/news-image-20261126-v2/rank.svg)
![reward](https://make.fun/badge/news-image-20261126/Hoppererin/news-image-20261126-v2/reward.svg)

One image that sums up the world's news of **Thursday 26 November 2026** —
a one-page newspaper, drawn from scratch.

[View the bounty on make.fun](https://make.fun/bounty/news-image-20261126)

## What is on the page

Three heroes, all verified and all still developing on the day itself:

1. **Ras Tanura claimed hit; two tankers strike Hormuz mines** — Houthis claim
   the 550,000-barrel-a-day Saudi refinery was hit; satellite images show black
   smoke; the coalition says four drones were shot down. Brent crude jumped 3.5%.
   Labelled a CLAIM — damage unconfirmed.
2. **Thirteen dead, thirteen trapped in an Indonesian mine** — rescuers returned
   at dawn to an illegal gold pit in West Java; thirteen bodies recovered,
   thirteen miners still underground.
3. **Kyiv hits two Russian refineries and an airfield** — Ukraine says it struck
   oil plants in Samara and a military airfield, downing 88 of 112 drones overnight.

Below them: six mid stories (Trump's tariffs on 14 partners, the Rosstat leak
putting Russian war dead at 490,334, the Cairo tanker fire, the Gaza strike,
the corrected Sudan toll of 19 civilians, the Netanyahu charges), twelve briefs
and twelve micro items — 33 stories in all, across every region.

A **CLAIMED vs CONFIRMED** box keeps the record honest: the refinery hit is a
claim, the Hormuz mine strikes are claimed by Iran and not independently
confirmed, and the Russian toll is a leak the Kremlin denies.

## How it is made

`render.py` draws the page with Python's Pillow (standard library + Pillow,
run locally at build time): Noto Serif/Sans type, flat-vector scenes per hero,
word-wrap measured against every box. It aborts if any text would be clipped
and prints `no truncations` on a clean run; two renders are byte-identical.

`main.ts` (Node 22, standard library only) copies `entry.png` to the output
directory and verifies the copy — PNG magic, 1024×1024, under 1 MiB, sha256
identical to the source.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`entry.png` is 1024×1024 RGB, under 1 MiB, deterministic.
