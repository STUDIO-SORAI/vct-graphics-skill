# vct-graphics-skill

An agent skill + script set for producing **VALORANT Champions Tour (VCT)** social graphics in Traditional Chinese: season maps, partner teams, slot allocations, qualification paths, LCQ, regional brackets, Kickoff slots and mega-thread covers for **Pacific / EMEA / Americas**. 1080×1350 portrait, exported @2x (2160×2700). Pure Python + Pillow.

> **Unofficial.** VALORANT and VCT are trademarks of Riot Games, Inc. This project is not affiliated with or endorsed by Riot Games (see [NOTICE](NOTICE)). The repo ships **code only**: no Riot/VCT marks, team logos, brand logos, fonts or photographs. You supply those (see [assets/README.md](assets/README.md)).

Licensed under the [Mozilla Public License 2.0](LICENSE).

## Use as an agent skill
Drop this repo (or its folder) into your agent's skills directory; [SKILL.md](SKILL.md) tells the agent when and how to use it, plus the house conventions.

## Setup
```bash
pip install pillow numpy scipy
# 1. add your assets exactly as listed in assets/README.md
# 2. render
REG=emea python3 scripts/reg.py slots 2 out/emea-slots.png
scripts/render_all.sh            # everything → ./out
```
Missing assets produce a clear error listing the files to add; backgrounds are generated on demand by `scripts/bg.py`. All paths resolve from the repo root (`VCT_ROOT` overrides).

## Scripts
| Script | Purpose |
|---|---|
| `scripts/reg.py` | Regional generator. `REG=pac|emea|amer python3 reg.py <mode> <S> <out>` |
| `scripts/kick_pac.py` | `reg.py` + the Pacific `kslots` (Kickoff slot allocation) mode |
| `scripts/pac.py` | Standalone Pacific Cup generator (`overview|partners|slots|path|lcq`) |
| `scripts/cover.py`, `hue.py` | Mega-thread covers (`cover1`, `cover2`); `hue.py` hue-rotates the Pacific background to red |
| `scripts/bg.py` | Procedural layered backgrounds (`pac`, `eu`, `euam`) |
| `scripts/_assets.py` | Asset preflight and friendly errors |
| `scripts/render_all.sh` | Render the whole set at 1x and @2x |

`S` = 1 or 2 (2 → @2x).

### `reg.py` modes
| Mode | Content |
|---|---|
| `overview` | Season map (Kickoff / Cup 1 / Cup 2 / Masters / Champions) — the only graphic with dates |
| `partners` | Partner teams of the region |
| `slots` | Cup slot allocation |
| `path` | Open-qualifier path to the Cup |
| `lcq` | 最終資格賽 |
| `br_eu` `br_tr` `br_mena` · `br_na` `br_br` `br_latam` | Regional qualifier brackets (雙敗淘汰); tree is indicative |
| `kslots` (`kick_pac.py`, `REG=pac`) | Pacific Kickoff slots |

## Brand colours
| Region | LIME (accent) | TINT | LCQC | LCO |
|---|---|---|---|---|
| Pacific | (198,244,50) | (6,18,30) | (24,92,120) | (120,200,225) |
| EMEA | (205,245,40) | (16,6,40) | (88,52,170) | (176,150,255) |
| Americas | (255,122,26) | (22,10,4) | (128,50,12) | (255,166,96) |

Shared: INK (22,22,22), white, MUT (160,170,176), GREY (222,226,228), CY (0,190,214).

## Adding a region
1. Add an entry to `CFG` in `scripts/reg.py` (`bg`, `lock`, `name`, `LIME`, `TINT`, `LCQC`, `LCO`, `coord`, `zone`).
2. Add a background variant to `scripts/bg.py` and the `BG_ARG` map in `scripts/_assets.py`; add the region lockup file name to `assets/README.md` and the preflight in `_assets.py`.
3. Add team logos under `assets/logos/…` and list the teams via `PT()`.
4. Fill the region's data blocks: overview `_B` entries (cities, dates, photo keys), `slots`, `path`, `lcq`, `br_*`.
5. Add the city photo `assets/photos/p_<key>.jpg` and note its credit in `assets/README.md`.
6. Add the region to `scripts/render_all.sh`.

## Adding a season
Update the “2027” title strings, event dates, partner lists, slot counts and bracket data, and re-verify every fact against Riot's official announcements before rendering. Backgrounds are procedural; lockups/logos can usually be reused.

## Conventions
- Source credit on graphics: 「來源：Riot Games」 (the first cover has none).
- Wording: 「Cup」 (not 盃賽), 「雙敗淘汰」, 「最終資格賽」; avoid 「站」 and 「至少」.
- No dates on format graphics (slots, path, LCQ, brackets); dates only on the overview.
- Minimal text on graphics; details go in the caption.
- Export @2x for delivery. Drive naming: `NN-<region>-<mode>.png`.
- Bracket trees are indicative, not official seeding.

## Known cosmetic defects
The VCT emblem tile in the Pacific/Americas lockups can have its right frame edge clipped (depends on your lockup file); EMEA graphics all carry the header “EUROPE KICKOFF”, including MENA.

## Licence
Code and documentation: MPL-2.0 (see [LICENSE](LICENSE), [NOTICE](NOTICE)). Third-party assets you add are under their own terms.
