# Prompt: VHB Streetmix sprite set

Paste this into Figma (Make / First Draft), or hand it to an illustrator. It describes the whole job; the table at the end is the full sprite list.

---

Redraw the complete sprite set for **Streetmix**, a street cross-section design tool, as a **VHB**-branded edition. Every sprite is a flat vector illustration seen straight-on (elevation view, no perspective), sitting on a ground line at the bottom edge of its box.

**Brand feel.** VHB is an engineering, planning and design firm; the brand is genuine, personable, forward-thinking, and about mobility, communities and environmental stewardship. The art should feel clean, optimistic and precise: a planner's diagram with warmth, not a cartoon.

**Signature shapes** (from the VHB logo and brand book):
- the *leaf / droplet*: a rectangle with two opposite corners swept fully round and the other two kept tight. Use it for tree canopies, clouds, lamp heads, headlights, people's torsos, window corners.
- *flowing curves* (the logo's "improving mobility" bands): three parallel wavy bands as the livery on buses, trams and trains.
- *squares in a grid* (the logo's "enhancing communities"): windows and building bays.
- Overlapping translucent leaf and square shapes for sky and water, as on the brand-book cover.

**Colour.** Use only these, plus light tints of them for shading:
- Core: Teal #006B6E, Aqua #00839B, Leaf Green #789B4A, Medium Gray #97989A, Cobalt #0071B9, Midnight Blue #272B67
- Bold, sparingly (people's clothes, flowers, lights, awnings): Plum #662F6C, Berry #8B1D41, Papaya #CE812D, Citron #B4CC43
- Neutral: Charcoal #212721, Espresso #3E2B2F, Dark Grey #5E5C5A, Light Grey #E5E5E5, white
- Glass is always Midnight Blue with one pale diagonal glint. Asphalt is Dark Grey. Sidewalk is Light Grey. Bike lane is Leaf Green. Bus lane is Berry. Tail lights Berry, turn signals Papaya. Vehicles are white with a Teal band and a thin Citron line.
- Road markings stay white, and centre lines stay traffic yellow (#F2C230): they are functional, not decorative.

**Rules.**
- Flat fills only: no outlines, no gradients inside sprites, no drop shadows, no text or lettering (use bars and blocks where a sign would have words). The only letter allowed is the "P" on the parking sign.
- Do not draw the VHB logo into any sprite.
- People are diverse in skin tone, age, ability and dress, drawn as simple geometric figures.
- Left/right pairs are mirror images, except anything that reads as a letter or number.
- Keep every sprite inside its box and touching the bottom edge where the original stands on the ground. Tiling pieces (surfaces, fence, grass, water, parking-lot strip, sky bands) must join seamlessly left to right.
- Scale: 24 px = 1 foot. A car is about 6 ft wide (145 px); an adult is about 5.5 ft tall (135 px).

**Deliver** three frames named `tiles-1` (2328 × 2050), `tiles-2` (1987 × 2546) and `tiles-3` (2500 × 2050) with a transparent background, each sprite a named group at the exact x, y below; plus `sky-front` (500 × 560) and `sky-rear` (500 × 240) cloud bands in white on transparent, and 31 people in 120 × 192 boxes. Exporting the three frames as PNG at 1x must give files the app can use without any code change.

## Sprite list (115 art objects)

**lots** (11)

| sprite | sheet | x, y | w × h px |
|---|---|---|---|
| lot-fence-right | tiles-1 | 1224, 19 | 96 × 177 |
| lot-fence-left | tiles-1 | 1344, 19 | 96 × 177 |
| lot-grass | tiles-1 | 1104, 163 | 96 × 33 |
| waterfront-left-edge | tiles-1 | 240, 246 | 240 × 186 |
| waterfront-left-repeat | tiles-1 | 0, 327 | 240 × 105 |
| waterfront-right-edge | tiles-1 | 0, 462 | 240 × 186 |
| waterfront-right-repeat | tiles-1 | 240, 543 | 240 × 105 |
| parking-lot-right-edge | tiles-3 | 1630, 24 | 432 × 576 |
| parking-lot-right-repeat | tiles-3 | 2062, 468 | 431 × 132 |
| parking-lot-left-edge | tiles-3 | 2062, 620 | 431 × 576 |
| parking-lot-left-repeat | tiles-3 | 1630, 1065 | 432 × 131 |

**furniture** (24)

| sprite | sheet | x, y | w × h px |
|---|---|---|---|
| wayfinding-sign-small | tiles-1 | 222, 26 | 35 × 207 |
| wayfinding-sign-medium | tiles-1 | 121, 31 | 68 × 202 |
| wayfinding-sign-large | tiles-1 | 0, 35 | 96 × 198 |
| bike-rack-sidewalk-right | tiles-1 | 1468, 105 | 137 × 81 |
| bike-rack-sidewalk-left | tiles-1 | 1611, 105 | 138 × 81 |
| bench-right | tiles-1 | 1874, 121 | 69 × 65 |
| bench-left | tiles-1 | 1945, 121 | 69 × 65 |
| bench-center | tiles-1 | 1784, 156 | 59 × 30 |
| bike-rack-parallel-left | tiles-1 | 1279, 348 | 59 × 84 |
| bike-rack-parallel-right | tiles-1 | 1372, 348 | 59 × 84 |
| bike-rack-road-right | tiles-1 | 1468, 357 | 137 × 81 |
| bike-rack-road-left | tiles-1 | 1611, 357 | 138 × 81 |
| lamp-modern-both | tiles-1 | 936, 576 | 384 × 716 |
| lamp-modern-right | tiles-1 | 1347, 576 | 285 × 716 |
| lamp-modern-left | tiles-1 | 1680, 576 | 280 × 716 |
| parklet-right | tiles-2 | 528, 849 | 191 × 145 |
| parklet-left | tiles-2 | 769, 849 | 190 × 145 |
| bollard | tiles-2 | 940, 1575 | 16 × 111 |
| divider-dome | tiles-2 | 889, 1675 | 22 × 11 |
| lamp-traditional-left | tiles-3 | 852, 1176 | 56 × 355 |
| lamp-traditional-right | tiles-3 | 964, 1176 | 56 × 355 |
| lamp-traditional-both | tiles-3 | 783, 1188 | 41 × 342 |
| banner-pride-left | tiles-3 | 1056, 1200 | 94 × 144 |
| banner-pride-right | tiles-3 | 1058, 1393 | 94 × 143 |

**markings** (27)

| sprite | sheet | x, y | w × h px |
|---|---|---|---|
| arrow-inbound-straight | tiles-1 | 751, 166 | 34 × 58 |
| arrow-outbound-straight | tiles-1 | 965, 166 | 36 × 57 |
| arrow-inbound-right-straight | tiles-1 | 2016, 281 | 56 × 71 |
| parking-stall-line-left | tiles-1 | 1106, 391 | 30 × 88 |
| arrow-inbound-grey-wide | tiles-1 | 751, 406 | 34 × 58 |
| arrow-outbound-grey-wide | tiles-1 | 965, 406 | 36 × 57 |
| arrow-inbound-right | tiles-1 | 2020, 409 | 46 × 55 |
| rail-tracks-dark | tiles-1 | 473, 1393 | 113 × 95 |
| rail-tracks-light | tiles-1 | 713, 1393 | 113 × 95 |
| center-line-yellow-right | tiles-2 | 788, 271 | 28 × 88 |
| center-line-yellow-left | tiles-2 | 840, 271 | 28 × 88 |
| arrow-outbound-left-straight | tiles-2 | 1217, 279 | 56 × 71 |
| arrow-outbound-right-straight | tiles-2 | 1440, 279 | 56 × 71 |
| arrow-inbound-left-straight | tiles-2 | 1001, 281 | 56 × 71 |
| parking-stall-line-right | tiles-2 | 688, 391 | 30 × 88 |
| lane-edge-line-right | tiles-2 | 808, 391 | 8 × 88 |
| lane-edge-line-left | tiles-2 | 840, 391 | 8 × 88 |
| sharrow-inbound | tiles-2 | 426, 402 | 62 × 66 |
| sharrow-outbound | tiles-2 | 545, 402 | 62 × 66 |
| arrow-inbound-left | tiles-2 | 1008, 408 | 51 × 56 |
| arrow-outbound-left | tiles-2 | 1224, 409 | 46 × 54 |
| arrow-outbound-right | tiles-2 | 1444, 409 | 46 × 54 |
| arrow-outbound-both | tiles-2 | 1554, 409 | 82 × 54 |
| arrow-inbound-both | tiles-2 | 1675, 409 | 81 × 55 |
| arrow-outbound-shared | tiles-2 | 1213, 511 | 94 × 88 |
| arrow-inbound-shared | tiles-2 | 1453, 511 | 94 × 88 |
| striped-buffer-hatching | tiles-2 | 768, 535 | 120 × 88 |

**vehicles** (17)

| sprite | sheet | x, y | w × h px |
|---|---|---|---|
| bus-rear-shared-lane | tiles-1 | 400, 680 | 254 × 241 |
| bus-front-shared-lane | tiles-1 | 678, 680 | 251 × 241 |
| car-rear | tiles-1 | 22, 801 | 145 × 120 |
| car-front | tiles-1 | 214, 801 | 145 × 120 |
| light-rail-front | tiles-1 | 432, 967 | 192 × 383 |
| light-rail-rear | tiles-1 | 672, 967 | 192 × 383 |
| truck-front | tiles-1 | 414, 1537 | 225 × 272 |
| truck-rear | tiles-1 | 710, 1537 | 191 × 272 |
| train-inception-secret | tiles-1 | 1981, 1640 | 311 × 361 |
| car-side-angled-left | tiles-1 | 917, 1879 | 326 × 121 |
| car-side-angled-right | tiles-1 | 1301, 1879 | 326 × 121 |
| car-rear-signal-left | tiles-1 | 33, 1880 | 158 × 120 |
| car-rear-signal-right | tiles-1 | 261, 1880 | 158 × 120 |
| car-front-signal-left | tiles-1 | 489, 1880 | 157 × 120 |
| car-front-signal-right | tiles-1 | 718, 1880 | 156 × 120 |
| streetcar-front | tiles-3 | 740, 2 | 249 × 317 |
| streetcar-rear | tiles-3 | 1028, 2 | 249 × 316 |

**nature** (4)

| sprite | sheet | x, y | w × h px |
|---|---|---|---|
| tree-palm | tiles-1 | 2001, 811 | 274 × 480 |
| tree-big | tiles-1 | 960, 1350 | 209 × 491 |
| flowers | tiles-2 | 912, 1456 | 48 × 45 |
| planter-box | tiles-2 | 984, 1593 | 96 × 93 |

**cyclists** (4)

| sprite | sheet | x, y | w × h px |
|---|---|---|---|
| cyclist-a-front | tiles-1 | 126, 1214 | 55 × 137 |
| cyclist-a-rear | tiles-1 | 223, 1214 | 53 × 137 |
| cyclist-b-front | tiles-1 | 126, 1454 | 55 × 137 |
| cyclist-b-rear | tiles-1 | 224, 1454 | 53 × 137 |

**buildings** (16)

| sprite | sheet | x, y | w × h px |
|---|---|---|---|
| building-narrow-left-roof | tiles-2 | 1042, 635 | 392 × 35 |
| building-narrow-right-roof | tiles-2 | 1508, 635 | 390 × 35 |
| building-narrow-left-upper-floor | tiles-2 | 1042, 670 | 384 × 240 |
| building-narrow-right-upper-floor | tiles-2 | 1517, 670 | 381 × 240 |
| building-narrow-left-ground-floor | tiles-2 | 1042, 910 | 412 × 337 |
| building-narrow-right-ground-floor | tiles-2 | 1488, 910 | 410 × 337 |
| building-home-right-roof | tiles-2 | 1560, 1732 | 390 × 140 |
| building-home-right-ground-floor | tiles-2 | 1221, 1872 | 729 × 588 |
| building-wide-left-roof | tiles-3 | 41, 536 | 736 × 40 |
| building-wide-right-roof | tiles-3 | 855, 541 | 735 × 33 |
| building-wide-right-upper-floor | tiles-3 | 855, 574 | 735 × 240 |
| building-wide-left-upper-floor | tiles-3 | 41, 576 | 727 × 240 |
| building-wide-right-ground-floor | tiles-3 | 833, 814 | 757 × 338 |
| building-wide-left-ground-floor | tiles-3 | 41, 816 | 753 × 337 |
| building-home-left-roof | tiles-3 | 1214, 1262 | 390 × 140 |
| building-home-left-ground-floor | tiles-3 | 1214, 1402 | 729 × 588 |

**surfaces** (8)

| sprite | sheet | x, y | w × h px |
|---|---|---|---|
| surface-light-rail-grey | tiles-2 | 624, 1062 | 216 × 90 |
| surface-divider-median | tiles-2 | 336, 1072 | 240 × 104 |
| ground-cover-grass | tiles-2 | 888, 1275 | 96 × 132 |
| surface-sidewalk-concrete | tiles-2 | 624, 1288 | 216 × 104 |
| surface-asphalt | tiles-2 | 336, 1302 | 240 × 90 |
| surface-bike-lane-green | tiles-2 | 96, 1542 | 192 × 90 |
| surface-bus-lane-red | tiles-2 | 336, 1542 | 240 × 90 |
| surface-transit-platform-raised | tiles-2 | 624, 1564 | 216 × 164 |

**transit** (4)

| sprite | sheet | x, y | w × h px |
|---|---|---|---|
| transit-shelter-street-left | tiles-3 | 220, 24 | 207 × 282 |
| transit-shelter-street-right | tiles-3 | 462, 24 | 207 × 282 |
| transit-shelter-light-rail-left | tiles-3 | 220, 1224 | 207 × 269 |
| transit-shelter-light-rail-right | tiles-3 | 463, 1224 | 206 × 269 |

**people** (31): `people-01` … `people-31`, 120 × 192 px each. 1–15 and 31 single adults; 16 with a cane; 17–18 with a walker; 19–20 wheelchair users; 21–22 children; 23–24 walking a dog; 25 child on a scooter; 26 and 28 adult with child; 27 with a white cane; 29 a couple; 30 carrying a baby.

**sky** (2): `sky-front`, `sky-rear`.

**Still to do after this set**: the ~45 small UI icons (building, direction, turn-lane, tree, lamp, bench and similar variant pickers), a favicon, and VHB project photos to replace the 20 "learn more" example photos.
