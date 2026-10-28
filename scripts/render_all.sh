#!/usr/bin/env bash
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Render the full set at 1x and @2x into ./out (needs the assets from assets/README.md).
set -e
cd "$(dirname "$0")"; mkdir -p ../out
O=../out
for S in 1 2; do sfx=$([ $S = 2 ] && echo '@2x' || echo '')
  for m in overview partners slots path lcq; do python3 pac.py $m $S $O/pacific-$m-45$sfx.png; done
  REG=pac python3 kick_pac.py kslots $S $O/pacific-kickoff-slots-45$sfx.png
  for m in overview partners slots path; do REG=emea python3 reg.py $m $S $O/emea-$m-45$sfx.png; done
  for m in overview partners slots path lcq; do REG=amer python3 reg.py $m $S $O/amer-$m-45$sfx.png; done
  for m in eu tr mena; do REG=emea python3 reg.py br_$m $S $O/emea-bracket-$m-45$sfx.png; done
  for m in na br latam; do REG=amer python3 reg.py br_$m $S $O/amer-bracket-$m-45$sfx.png; done
  for m in cover1 cover2; do python3 cover.py $m $S $O/cover-0${m: -1}$sfx.png; done
done
echo done
