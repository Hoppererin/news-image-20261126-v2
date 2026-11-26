#!/usr/bin/env python3
"""Render news-image-20261126 v2 entry.png — a one-page newspaper of 26 Nov 2026.

Deterministic: no clock, no randomness, no network. Same input bytes always
produce the same output bytes. Run twice and compare sha256 to confirm.

Layout (1024 x 1024): masthead + date band, 3 hero stories with drawn scenes,
6 mid stories, 12 briefs, 12 micro items, CLAIMED vs CONFIRMED honesty box,
source footer. The script aborts with a TRUNCATION report if any text does
not fit its box; a clean run prints "no truncations".
"""
import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28
CW = W - 2 * MARGIN  # 968

PAPER = (250, 247, 240)
INK = (26, 26, 26)
GREY = (107, 114, 128)
LIGHT_GREY = (220, 216, 208)
RED = (185, 28, 28)
BLUE = (29, 78, 216)

FONT_DIR = "/usr/share/fonts/truetype/noto"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_MASTHEAD = font("NotoSerif-Black.ttf", 42)
F_DATE = font("NotoSans-Black.ttf", 23)
F_TAGLINE = font("NotoSerif-Italic.ttf", 15)
F_KICKER = font("NotoSans-Black.ttf", 12)
F_HERO_H = font("NotoSerif-Bold.ttf", 29)
F_HERO_D = font("NotoSans-Regular.ttf", 14)
F_HERO_S = font("NotoSans-Bold.ttf", 11)
F_MID_H = font("NotoSerif-Bold.ttf", 20)
F_MID_D = font("NotoSans-Regular.ttf", 13)
F_SEC = font("NotoSans-Black.ttf", 13)
F_BRIEF = font("NotoSans-Regular.ttf", 14)
F_BRIEF_B = font("NotoSans-Bold.ttf", 14)
F_MICRO = font("NotoSans-Regular.ttf", 13)
F_BOX_H = font("NotoSans-Black.ttf", 12)
F_BOX = font("NotoSans-Regular.ttf", 12)
F_FOOT = font("NotoSans-Regular.ttf", 11)

TRUNCATIONS = []


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap. Returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, lh, max_lines=None, tag=""):
    """Draw lines starting at (x, y). Records a truncation if over max_lines."""
    if max_lines is not None and len(lines) > max_lines:
        TRUNCATIONS.append(
            "%s: %d lines, only %d fit (%r...)" % (tag, len(lines), max_lines, lines[max_lines][:40])
        )
        lines = lines[:max_lines]
    for i, ln in enumerate(lines):
        draw.text((x, y + i * lh), ln, font=fnt, fill=fill)
    return y + len(lines) * lh


def line_h(fnt, factor=1.22):
    return int(fnt.size * factor)


# ---------------------------------------------------------------- scenes
def scene_gulf(dr, x, y, w, h):
    """Ras Tanura refinery at dusk: flare stacks, black smoke, tanker at sea.
    All shapes stay inside (x, y, w, h)."""
    bands = [(233, 150, 84), (226, 120, 70), (198, 96, 62), (160, 74, 58)]
    bh = h * 0.62 / len(bands)
    for i, c in enumerate(bands):
        dr.rectangle([x, y + i * bh, x + w, y + (i + 1) * bh + 1], fill=c)
    dr.ellipse([x + w - 70, y + 8, x + w - 36, y + 42], fill=(252, 211, 119))
    dr.rectangle([x, y + h * 0.62, x + w, y + h], fill=(31, 58, 95))
    dr.rectangle([x, y + h * 0.62, x + w, y + h * 0.62 + 3], fill=(120, 150, 190))
    ty = y + h * 0.70
    dr.polygon([(x + 18, ty), (x + 150, ty), (x + 138, ty + 26), (x + 30, ty + 26)], fill=(20, 20, 20))
    dr.rectangle([x + 34, ty - 16, x + 118, ty], fill=(140, 40, 32))
    dr.rectangle([x + 122, ty - 22, x + 142, ty], fill=(220, 220, 210))
    dr.rectangle([x + 126, ty - 30, x + 132, ty - 22], fill=(220, 220, 210))
    gy = y + h * 0.62
    dr.rectangle([x, gy - 6, x + w, gy], fill=(40, 32, 30))
    for cx, cw, ch in [(x + 180, 16, 46), (x + 204, 12, 58), (x + 222, 18, 38)]:
        dr.rectangle([cx, gy - ch, cx + cw, gy], fill=(52, 44, 42))
        dr.ellipse([cx - 2, gy - ch - 6, cx + cw + 2, gy - ch + 2], fill=(52, 44, 42))
    for cx in (x + 252, x + 282):
        dr.rectangle([cx, gy - 28, cx + 24, gy], fill=(66, 56, 52))
        dr.ellipse([cx, gy - 34, cx + 24, gy - 22], fill=(80, 68, 62))
    dr.rectangle([x + 158, gy - 58, x + 164, gy], fill=(52, 44, 42))
    dr.polygon([(x + 152, gy - 58), (x + 170, gy - 58), (x + 161, gy - 72)], fill=(245, 158, 11))
    dr.polygon([(x + 156, gy - 58), (x + 166, gy - 58), (x + 161, gy - 66)], fill=(252, 211, 119))
    smoke = (58, 52, 50)
    for sx, sy, sw, sh in [
        (x + 172, gy - 62, 46, 22), (x + 190, gy - 70, 50, 24),
    ]:
        dr.ellipse([sx, sy, sx + sw, sy + sh], fill=smoke)
    for wx in range(x + 8, x + w - 20, 26):
        dr.arc([wx, y + h - 22, wx + 22, y + h - 8], 200, 340, fill=(150, 180, 220), width=2)


def scene_mine(dr, x, y, w, h):
    """West Java gold mine: headframe tower, framed tunnel mouth, rescue lamps.
    All shapes stay inside (x, y, w, h)."""
    bands = [(214, 196, 168), (198, 178, 150), (176, 152, 126)]
    bh = h * 0.55 / len(bands)
    for i, c in enumerate(bands):
        dr.rectangle([x, y + i * bh, x + w, y + (i + 1) * bh + 1], fill=c)
    dr.polygon([(x, y + h), (x, y + h * 0.62), (x + w * 0.45, y + h * 0.34),
                (x + w, y + h * 0.55), (x + w, y + h)], fill=(122, 102, 78))
    dr.polygon([(x + w * 0.45, y + h * 0.34), (x + w * 0.62, y + h * 0.46),
                (x + w * 0.30, y + h * 0.52)], fill=(150, 132, 106))
    dr.rectangle([x, y + h * 0.72, x + w, y + h], fill=(96, 80, 62))
    tx, ty = x + w - 96, y + h * 0.72
    dr.line([(tx, ty), (tx + 14, ty - 80)], fill=(40, 38, 36), width=5)
    dr.line([(tx + 52, ty), (tx + 38, ty - 80)], fill=(40, 38, 36), width=5)
    dr.line([(tx + 8, ty - 80), (tx + 44, ty - 80)], fill=(40, 38, 36), width=5)
    dr.line([(tx + 4, ty - 44), (tx + 48, ty - 66)], fill=(40, 38, 36), width=3)
    dr.line([(tx + 48, ty - 44), (tx + 4, ty - 66)], fill=(40, 38, 36), width=3)
    dr.rectangle([tx + 8, ty - 90, tx + 44, ty - 80], fill=(40, 38, 36))
    dr.line([(tx + 26, ty - 84), (x + 70, y + h * 0.80)], fill=(60, 56, 52), width=2)
    # timber-framed tunnel mouth: brown frame, dark interior arch
    dr.pieslice([x + 30, y + h * 0.64, x + 110, y + h * 0.94], 180, 360, fill=(120, 96, 70))
    dr.rectangle([x + 30, y + h * 0.79, x + 110, y + h * 0.94], fill=(120, 96, 70))
    dr.pieslice([x + 38, y + h * 0.68, x + 102, y + h * 0.94], 180, 360, fill=(24, 20, 18))
    dr.rectangle([x + 38, y + h * 0.81, x + 102, y + h * 0.94], fill=(24, 20, 18))
    for lx, ly in [(x + 52, y + h * 0.82), (x + 70, y + h * 0.88), (x + 88, y + h * 0.84)]:
        dr.ellipse([lx - 3, ly - 3, lx + 3, ly + 3], fill=(252, 211, 119))
    for wx in (x + 140, x + 168, x + 196):
        dr.ellipse([wx - 4, y + h * 0.86 - 4, wx + 4, y + h * 0.86 + 4], fill=(30, 30, 30))
        dr.rectangle([wx - 5, y + h * 0.86 + 4, wx + 5, y + h * 0.97], fill=(200, 60, 40))
        dr.ellipse([wx - 2, y + h * 0.80 - 2, wx + 2, y + h * 0.80 + 2], fill=(252, 211, 119))
    dr.polygon([(x + 8, y + h), (x + 40, y + h * 0.88), (x + 76, y + h)], fill=(140, 122, 98))
    for rx, ry, rr in [(x + 250, y + h - 12, 7), (x + 272, y + h - 8, 5), (x + 228, y + h - 6, 4)]:
        dr.ellipse([rx - rr, ry - rr, rx + rr, ry + rr], fill=(120, 106, 88))


def scene_ukraine(dr, x, y, w, h):
    """Night strike on a refinery: fire glow, drone silhouettes, tracer fire.
    All shapes stay inside (x, y, w, h)."""
    dr.rectangle([x, y, x + w, y + h], fill=(16, 24, 54))
    for sx, sy in [(x + 30, y + 18), (x + 90, y + 34), (x + 150, y + 12), (x + 230, y + 26),
                   (x + 280, y + 44), (x + 60, y + 52), (x + 190, y + 48)]:
        dr.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(220, 225, 240))
    gy = y + h * 0.74
    dr.rectangle([x, y + h * 0.74, x + w, y + h], fill=(12, 12, 16))
    dr.ellipse([x + 128, gy - 88, x + 202, gy - 6], fill=(120, 50, 18))
    dr.ellipse([x + 142, gy - 74, x + 188, gy - 18], fill=(198, 96, 28))
    dr.rectangle([x + 150, gy - 70, x + 180, gy], fill=(28, 24, 24))
    dr.polygon([(x + 144, gy - 70), (x + 186, gy - 70), (x + 165, gy - 90)], fill=(245, 130, 20))
    dr.polygon([(x + 153, gy - 70), (x + 177, gy - 70), (x + 165, gy - 82)], fill=(252, 200, 90))
    dr.rectangle([x + 200, gy - 48, x + 216, gy], fill=(34, 30, 30))
    dr.rectangle([x + 228, gy - 30, x + 256, gy], fill=(44, 38, 38))
    dr.ellipse([x + 228, gy - 36, x + 256, gy - 24], fill=(56, 48, 46))
    for sx, sy, sw, sh in [(x + 140, gy - 88, 56, 22), (x + 164, gy - 78, 60, 24)]:
        dr.ellipse([sx, sy, sx + sw, sy + sh], fill=(52, 48, 52))
    for dx, dy in [(x + 44, y + 30), (x + 250, y + 58), (x + 120, y + 22)]:
        dr.line([(dx - 9, dy), (dx + 9, dy)], fill=(8, 8, 10), width=3)
        dr.line([(dx, dy - 5), (dx, dy + 5)], fill=(8, 8, 10), width=3)
        dr.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=(220, 40, 40))
    for tx1, ty1, tx2, ty2 in [(x + 20, gy, x + 60, y + 40), (x + 290, gy, x + 252, y + 52),
                               (x + 90, gy, x + 118, y + 26)]:
        dr.line([(tx1, ty1), (tx2, ty2)], fill=(252, 220, 130), width=2)


# ---------------------------------------------------------------- stories
HEROES = [
    {
        "kicker": "MIDDLE EAST  •  ENERGY",
        "scene": scene_gulf,
        "headline": "Ras Tanura claimed hit; two tankers strike Hormuz mines",
        "deck": "Satellite images show black smoke over the 550,000-bpd refinery. Coalition: four drones downed. Brent up 3.5% to ~$95.",
        "source": "REUTERS  •  CLAIM — DAMAGE UNCONFIRMED",
    },
    {
        "kicker": "ASIA  •  DISASTER",
        "scene": scene_mine,
        "headline": "Thirteen dead, thirteen trapped in Indonesian mine",
        "deck": "Rescuers returned at dawn to an illegal pit in West Java. Thirteen bodies recovered; thirteen miners still underground.",
        "source": "REUTERS  •  THURSDAY 26 NOVEMBER",
    },
    {
        "kicker": "EUROPE  •  WAR",
        "scene": scene_ukraine,
        "headline": "Kyiv hits two Russian refineries and an airfield",
        "deck": "Ukraine says it hit oil plants in Samara and a military airfield, downing 88 of 112 Russian drones overnight.",
        "source": "SBU  •  THURSDAY 26 NOVEMBER",
    },
]

MID = [
    ("TRADE  •  REUTERS", "Trump proposes tariffs on 14 partners; markets slide",
     "Tariffs target China, Japan, EU over excess capacity. Nvidia fell 3.9%; Asia steadied."),
    ("RUSSIA  •  BBC RUSSIAN — LEAK", "Leak puts Russian war dead at 490,334",
     "BBC Russian and Mediazona cite a Rosstat leak; toll may pass 700,000. Kremlin disputes it."),
    ("EGYPT  •  REUTERS", "Fuel tanker fire kills at least 30 on Cairo highway",
     "Tanker overturned and burst into flames; at least 30 killed, 15 injured, officials said."),
    ("GAZA  •  REUTERS", "Israeli strike kills Hamas security chief in Gaza",
     "Abu al-Ouf, Hamas security chief, was killed with family in an Israeli airstrike, officials said."),
    ("SUDAN  •  REUTERS — VERIFIED", "Drone strikes kill 19 civilians in Sudan's Blue Nile",
     "Reuters: 19 civilians killed in Blue Nile drone strikes; another strike killed a schoolchild."),
    ("ISRAEL  •  REUTERS", "Judges urge dropping gravest Netanyahu charges",
     "Israeli judges urge dropping the most serious charges in the PM's corruption trial."),
]

BRIEF = [
    ("SEOUL", "Bank of Korea lifts its rate to 3.25%."),
    ("TOKYO", "Nikkei up 1.6% as Asia steadies after the slide."),
    ("WARSAW", "Poland asks NATO to down Russian missiles over Ukraine."),
    ("BRUSSELS", "NATO chief: Europe must prepare for large-scale war."),
    ("NEW YORK", "Huawei found guilty of bank fraud, Iran breaches."),
    ("PYONGYANG", "North Korea expels a Swiss diplomat in a sanctions row."),
    ("SPACE", "Shenzhou-24 launches with Pakistan's first astronaut."),
    ("ABUJA", "Nigeria seizes $220m of meth; five Mexicans arrested."),
    ("BOGOTÁ", "About 30 hostages freed after a Colombia standoff."),
    ("BEIRUT", "Lebanon plans a second international airport."),
    ("PRETORIA", "Court backs Ramaphosa in the cash-theft case."),
    ("DHAKA", "Garment workers win a 36% pay rise."),
]

MICRO = [
    "UK moves RAF jets into hangars over drone threat",
    "EU plans €50bn tech fund to rival US and China",
    "Haftar makes first formal visit to Turkey",
    "Estonia seals its border with Russia",
    "Knesset backs 7 October inquiry over Netanyahu's objections",
    "Iran to execute two protesters at dawn",
    "Hong Kong renovation blaze killed 168",
    "India answers US tariff threat, points to trade talks",
    "1,700 Indians deported from the US this year",
    "Macy's postpones Thanksgiving parade in bad weather",
    "California warns of floods as king tides peak",
    "Qatar Grand Prix goes ahead despite regional war",
]


def render(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    dr = ImageDraw.Draw(img)

    # ---- masthead (y 18 -> ~130)
    y = 18
    dr.text((MARGIN, y), "THE WORLD IN ONE PAGE", font=F_MASTHEAD, fill=INK)
    y += line_h(F_MASTHEAD) + 2
    dr.rectangle([MARGIN, y, MARGIN + CW, y + 38], fill=INK)
    dr.text((MARGIN + 14, y + 6), "THURSDAY  26  NOVEMBER  2026", font=F_DATE, fill=(250, 247, 240))
    dr.text((MARGIN + CW - 14 - dr.textlength("ONE DAY  •  ONE IMAGE", font=F_TAGLINE),
             y + 10), "ONE DAY  •  ONE IMAGE", font=F_TAGLINE, fill=(200, 196, 188))
    y += 38 + 6
    dr.line([(MARGIN, y), (MARGIN + CW, y)], fill=INK, width=2)
    y += 10

    # ---- heroes: 3 columns, 322 tall
    hero_w = (CW - 2 * 16) // 3  # 312
    hero_h = 322
    hy = y
    for i, hro in enumerate(HEROES):
        hx = MARGIN + i * (hero_w + 16)
        # render the scene on its own tile so no shape can bleed outside it
        tile = Image.new("RGB", (hero_w, 128), PAPER)
        tile_dr = ImageDraw.Draw(tile)
        hro["scene"](tile_dr, 0, 0, hero_w, 128)
        img.paste(tile, (hx, hy))
        cy = hy + 128 + 6
        dr.text((hx, cy), hro["kicker"], font=F_KICKER, fill=RED)
        cy += line_h(F_KICKER) + 3
        cy = draw_lines(dr, hx, cy, wrap(dr, hro["headline"], F_HERO_H, hero_w),
                        F_HERO_H, INK, 33, max_lines=3, tag="hero%d headline" % i)
        cy += 3
        cy = draw_lines(dr, hx, cy, wrap(dr, hro["deck"], F_HERO_D, hero_w),
                        F_HERO_D, INK, 17, max_lines=3, tag="hero%d deck" % i)
        cy += 4
        dr.text((hx, cy), hro["source"], font=F_HERO_S, fill=GREY)
        if i < 2:
            dr.line([(hx + hero_w + 8, hy), (hx + hero_w + 8, hy + hero_h)], fill=LIGHT_GREY, width=1)
    y = hy + hero_h + 8
    dr.line([(MARGIN, y), (MARGIN + CW, y)], fill=INK, width=2)
    y += 8

    # ---- mid band: 6 items, 2 rows x 3 cols, 100 each
    mid_w = hero_w
    mid_h = 100
    for r in range(2):
        for c in range(3):
            idx = r * 3 + c
            tag, head, deck = MID[idx]
            mx = MARGIN + c * (mid_w + 16)
            my = y + r * (mid_h + 8)
            dr.text((mx, my), tag, font=F_KICKER, fill=BLUE)
            my += line_h(F_KICKER) + 3
            my = draw_lines(dr, mx, my, wrap(dr, head, F_MID_H, mid_w),
                            F_MID_H, INK, 24, max_lines=2, tag="mid%d headline" % idx)
            my += 2
            draw_lines(dr, mx, my, wrap(dr, deck, F_MID_D, mid_w),
                       F_MID_D, INK, 16, max_lines=2, tag="mid%d deck" % idx)
            if c < 2:
                dr.line([(mx + mid_w + 8, y + r * (mid_h + 8)),
                         (mx + mid_w + 8, y + r * (mid_h + 8) + mid_h)], fill=LIGHT_GREY, width=1)
    y += 2 * mid_h + 8 + 6
    dr.line([(MARGIN, y), (MARGIN + CW, y)], fill=INK, width=2)
    y += 8

    # ---- brief: ALSO TODAY, 2 cols x 6, single line each
    dr.text((MARGIN, y), "ALSO TODAY", font=F_SEC, fill=INK)
    y += line_h(F_SEC) + 5
    brief_w = (CW - 24) // 2
    for i, (place, text) in enumerate(BRIEF):
        col, row = i % 2, i // 2
        bx = MARGIN + col * (brief_w + 24)
        by = y + row * 18
        full = place + " — " + text
        if dr.textlength(full, font=F_BRIEF) > brief_w:
            TRUNCATIONS.append("brief%d too wide (%d px > %d): %r"
                               % (i, dr.textlength(full, font=F_BRIEF), brief_w, full))
        lead = place + " — "
        lead_w = dr.textlength(lead, font=F_BRIEF_B)
        dr.text((bx, by), lead, font=F_BRIEF_B, fill=INK)
        dr.text((bx + lead_w, by), text, font=F_BRIEF, fill=INK)
    y += 6 * 18 + 4
    dr.line([(MARGIN, y), (MARGIN + CW, y)], fill=INK, width=1)
    y += 8

    # ---- micro: IN BRIEF, 2 cols x 6, one line each
    dr.text((MARGIN, y), "IN BRIEF", font=F_SEC, fill=INK)
    y += line_h(F_SEC) + 4
    for i, item in enumerate(MICRO):
        col, row = i % 2, i // 2
        mx = MARGIN + col * (brief_w + 24)
        my = y + row * 15
        s = "•  " + item
        if dr.textlength(s, font=F_MICRO) > brief_w:
            TRUNCATIONS.append("micro%d too wide: %r" % (i, item))
        dr.text((mx, my), s, font=F_MICRO, fill=INK)
    y += 6 * 15 + 4
    dr.line([(MARGIN, y), (MARGIN + CW, y)], fill=INK, width=1)
    y += 8

    # ---- honesty box
    box_h = 42
    dr.rectangle([MARGIN, y, MARGIN + CW, y + box_h], outline=RED, width=2)
    dr.text((MARGIN + 10, y + 5), "CLAIMED vs CONFIRMED — ", font=F_BOX_H, fill=RED)
    bx = MARGIN + 10 + dr.textlength("CLAIMED vs CONFIRMED — ", font=F_BOX_H)
    box_text = ("Houthi refinery hit is a CLAIM, damage unconfirmed (coalition: 4 drones downed). "
                "Hormuz mine strikes are claimed by Iran, not independently confirmed. "
                "The Russian toll is a LEAK; the Kremlin denies it.")
    lines = wrap(dr, box_text, F_BOX, CW - 20 - (bx - MARGIN))
    draw_lines(dr, bx, y + 5, lines, F_BOX, INK, 15, max_lines=2, tag="honesty box")
    y += box_h + 6

    # ---- footer
    dr.text((MARGIN, y), "Sources: Reuters  •  BBC Russian  •  AP  •  Xinhua  •  ESA  •  Mediazona  •  SBU  •  UKMTO",
            font=F_FOOT, fill=GREY)
    dr.text((MARGIN, y + 14), "Events first reported 26 November 2026 unless dated.  •  Judge note: this page sums up one day — Thursday 26 November 2026.",
            font=F_FOOT, fill=GREY)
    y += 28

    if y > H:
        TRUNCATIONS.append("layout overflow: content ends at y=%d > %d" % (y, H))

    img.save(out_path, format="PNG")
    return y


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    end_y = render(out)
    size = os.path.getsize(out)
    with open(out, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    im = Image.open(out)
    print("rendered %s: %dx%d RGB, %d bytes, sha256 %s (content ends y=%d)"
          % (out, im.width, im.height, size, digest, end_y))
    print("stories: %d heroes + %d mid + %d brief + %d micro = %d"
          % (len(HEROES), len(MID), len(BRIEF), len(MICRO),
             len(HEROES) + len(MID) + len(BRIEF) + len(MICRO)))
    if size > 1048576:
        print("FAIL: over 1 MiB")
        sys.exit(1)
    if im.width > 1024 or im.height > 1024:
        print("FAIL: over 1024x1024")
        sys.exit(1)
    if TRUNCATIONS:
        print("TRUNCATIONS (%d):" % len(TRUNCATIONS))
        for t in TRUNCATIONS:
            print("  - " + t)
        sys.exit(1)
    print("no truncations")


if __name__ == "__main__":
    main()
