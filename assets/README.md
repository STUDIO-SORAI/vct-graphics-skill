# assets/ — what to drop in, and where

This directory is **empty on purpose** (everything except this file is git-ignored). The repository contains
no Riot Games / VCT marks, no team logos, no SORAI logos, no fonts and no photographs. Supply them yourself,
lawfully, with the exact names below. If something is missing, the scripts stop with
`ERROR: missing asset file: <path>` (they never render a half-broken image).

Backgrounds (`bg_pac`, `bg_eu`, `bg_euam`, and their `@2x`) need nothing from you: they are procedural
and are generated automatically by `scripts/bg.py` on first render (or run
`python3 scripts/bg.py pac 1 assets/bg_pac.png`; use `2` and `bg_pac@2x.png` for the @2x file).

## 1. Fonts → `assets/fonts/ClashDisplay/`
| File | Source |
|---|---|
| `ClashDisplay-Bold.otf`, `ClashDisplay-Semibold.otf` | Fontshare — https://www.fontshare.com/fonts/clash-display (download yourself; do not redistribute) |

System fonts (not in this directory): **Noto Sans CJK** at
`/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc` and `-Regular.ttc` (`apt install fonts-noto-cjk`; the scripts use
face index 3 = TC), and for the covers **JetBrains Mono** variable
(`MONO` in `scripts/cover.py`). Both are SIL OFL 1.1.

## 2. Marks and lockups → `assets/`
| File | What it is | Used by |
|---|---|---|
| `vct_white.png` | White VCT emblem, transparent PNG (~492×524) | every script |
| `pacific_kickoff_white.png` | White "VCT Pacific" lockup, transparent (~921×238) | `REG=pac`, `pac.py` |
| `europe_kickoff_white.png` | White "VCT EMEA/Europe" lockup (~559×147) | `REG=emea` |
| `americas_kickoff_white.png` | White "VCT Americas" lockup (~921×238) | `REG=amer` |
| `sorai_logo_on_dark.png` | Your own studio/brand wordmark, white-on-transparent (~593×157), drawn bottom-left. Use any logo you like with this name | every script |

These are Riot's marks: use them under Riot's own policies.

## 3. Cover emblems → `assets/cover/`
`logo_pac.png`, `logo_emea.png`, `logo_amer.png` — white transparent region emblems (~221×238, 137×143, 221×238),
used only by `scripts/cover.py`.

## 4. Team logos → `assets/logos/pac/` and `assets/logos/am/`
Transparent PNGs. The filename suffix (`darkmode`/`lightmode`/`allmode`) is the variant that reads on the dark/light tile.
Tip: Liquipedia's team pages offer these variants; check their licence/terms and the team's brand rules.

`assets/logos/pac/` (Pacific + EMEA teams):
`Rex_Regum_Qeon_allmode.png`, `ZETA_DIVISION_darkmode.png`, `Gen.G_Esports_2026_allmode.png`, `T1_2019_allmode.png`,
`GAM_Esports_2021_full_allmode.png`, `Crazy_Raccoon_2021_allmode.png`, `FULL_SENSE_2025_allmode.png`, `Paper_Rex_darkmode.png`,
`Team_Heretics_2024_allmode.png`, `Fnatic_2020_allmode.png`, `Team_Vitality_2023_darkmode.png`, `Team_Liquid_2024_darkmode.png`,
`Gentle_Mates_2024_lightmode.png`, `Karmine_Corp_2024_darkmode.png`, `BBL_Esports_2022_darkmode.png`, `Futbolist_2021_darkmode.png`

`assets/logos/am/` (Americas teams):
`100_Thieves_darkmode.png`, `G2_Esports_2020_lightmode.png`, `NRG_2024_allmode.png`, `Sentinels_V_white.png`,
`LOUD_allmode.png`, `MIBR_2018_darkmode.png`, `Leviatan_2023_icon_allmode.png`, `KRU_Esports_allmode.png`

(Team lists change every season — to use different teams, edit the `PT()` calls in `scripts/reg.py` / `pac.py` and drop the new files in.)

## 5. City photos → `assets/photos/`
JPEGs named `p_<key>.jpg` (the scripts crop them; ~1600px wide landscape is plenty). Used for the season map and covers.
These are Wikimedia Commons files; each has its own licence, and CC BY / BY-SA files need attribution wherever you publish.

| File | City | Commons file | Author — licence |
|---|---|---|---|
| `p_bkk.jpg` | Bangkok | `File:Bangkok, Thailand, Sukhumvit Skyline, 2024.jpg` | OPK-Photography — CC BY-SA 4.0 |
| `p_seo.jpg` | Seoul | `File:Han River Seoul skyline Pixabay 1214950.jpg` | USAGI_POST — CC0 |
| `p_mnl.jpg` | Manila | `File:Manila Bay at Night.jpg` | Ralff Nestor Nacor — CC BY-SA 4.0 |
| `p_vlc.jpg` | Valencia | `File:City of Arts and Sciences Valencia in 2014.jpg` | Choinowski — CC BY-SA 4.0 |
| `p_tyo.jpg` | Tokyo | `File:Minato City, Tokyo, Japan.jpg` | David Kernan — CC BY 4.0 |
| `p_aus.jpg` | Austin | `File:Austin August 2019 19 (skyline and Lady Bird Lake).jpg` | Michael Barera — CC BY-SA 4.0 |
| `p_ber.jpg` | Berlin | `File:Berlin-SKY.jpg` | Sylla — CC0 |
| `p_war.jpg` | Warsaw | `File:Warsaw skyline from Al. Jerozolimskie (27th March 2025) 001.jpg` | Mtaylor848 — CC BY-SA 4.0 |
| `p_ist.jpg` | Istanbul | `File:Historical peninsula and modern skyline of Istanbul.jpg` | Hunanuk — CC0 |
| `p_sao.jpg` | São Paulo | `File:São Paulo skyline at Vila Mariana.jpg` | Rodrigo Tetsuo Argenton — CC BY-SA 4.0 |
| `p_mex.jpg` | Mexico City | `File:Mexico City Reforma skyline.jpg` | Jonathan Salvador — CC BY-SA 4.0 |
| `p_rio.jpg` | Rio de Janeiro | `File:Rio de Janeiro skyline and Sugarloaf Mountain at sunset, Brazil 3.jpg` | Wilfredor — CC0 |

Find a file at `https://commons.wikimedia.org/wiki/File:<name with underscores>`, download the original, save under the
name above. Verify each file's licence on its Commons page before use (it can change or be corrected).

## Resulting tree
```
assets/
  fonts/ClashDisplay/{ClashDisplay-Bold.otf,ClashDisplay-Semibold.otf}
  vct_white.png  pacific_kickoff_white.png  europe_kickoff_white.png  americas_kickoff_white.png  sorai_logo_on_dark.png
  cover/{logo_pac,logo_emea,logo_amer}.png
  logos/pac/*.png   logos/am/*.png
  photos/p_*.jpg
  bg_*.png          (generated)
```
