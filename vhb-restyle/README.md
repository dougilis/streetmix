# VHB Streetmix restyle kit

Everything needed to reskin Streetmix in the VHB brand: the original graphics pulled apart and named, the VHB palette, and a complete redrawn sprite set that sits at the exact pixel positions the app already reads.

Figma file: https://www.figma.com/design/9fos3MOyiRGBFoWqXyMX1U

![Street scene preview](vhb/preview/street-scene.png)

The scene above is a mock-up composed from the new art, not a capture of the running app.

## What the app draws, and where it comes from

| Graphic | Count | Source in the app |
|---|---|---|
| Segment sprites (vehicles, markings, furniture, trees, surfaces, shelters) | 97 crops | `public/images/tiles-1/2/3.png`, coordinates in `assets/scripts/segments/info.js` |
| Buildings and lots (narrow, wide, home, parking lot, waterfront, fence, grass) | 29 crops | same sheets, coordinates hard-coded in `assets/scripts/segments/buildings.js` |
| Sky | 2 | `public/images/sky-front.png`, `sky-rear.png`, plus `$sky-colour` in `assets/css/_variables.scss` |
| Sidewalk people | 31 | SVG symbols `people--people-01..31` from the external `streetmix-illustrations` package |
| UI icons | about 45 | external `streetmix-icons` package (ids listed in `assets/scripts/segments/variant_icons.js`) |
| "Learn more" photos | 20 | `public/images/info-bubble-examples/*.jpg` |
| UI colours and fonts | | `assets/css/_variables.scss`, `public/fonts` (Lato, Interstate, Roadgeek) |

Several crops share the same pixels (a parked car is a narrower crop of the same car, the home's upper floor is the top of its ground-floor sprite), so the 126 sheet crops come down to **115 distinct drawings**.

## What is in this folder

| Path | What it is |
|---|---|
| `manifest.json` | Every crop the app makes: name, sheet, pixel rectangle, and which segment variants use it |
| `art-objects.json` | The 115 distinct drawings with their exact footprint on each sheet |
| `original/` | The untouched sheets, each sprite sliced into its own named PNG, and a contact sheet |
| `brand-tokens.json` | VHB colours and fonts from the brand book, plus a suggested mapping for the app's SCSS colour variables |
| `vhb/sheets/tiles-1/2/3.svg` and `.png` | The redrawn sheets, same size and layout as the originals |
| `vhb/sprites/` | Each redrawn sprite as its own SVG |
| `vhb/people/`, `vhb/sky/` | 31 people and the two cloud bands |
| `vhb/preview/` | The street-scene mock-up and a before/after of sheet 1 |
| `FIGMA-PROMPT.md` | A self-contained brief for regenerating or extending the set in Figma or with an illustrator |
| `tools/` | The generator. Change a colour in `svgkit.py` or a drawing in `art_*.py` and rerun |

## Regenerating

```bash
python3 tools/generate.py
```

```bash
node tools/render.js --probe
```

```bash
python3 tools/fit.py
```

```bash
python3 tools/generate.py
```

```bash
python3 tools/preview.py
```

```bash
node tools/render.js
```

The middle steps measure each sprite and nudge any that spill outside their footprint. Needs Python 3 with Pillow, and Node with Playwright.

## Design calls made

- **Shapes** come from the logo and the brand-book cover: the leaf/droplet for canopies, clouds, lamp heads, headlights and torsos; the three "mobility" curves as vehicle livery; square window grids.
- **Colour roles**: glass Midnight Blue, asphalt Dark Grey, sidewalk Light Grey, bike lane Leaf Green, bus lane Berry, vehicles white with a Teal band.
- **The VHB logo is not drawn into any sprite.**
- **Road markings stay white and traffic yellow.** The yellow is not a brand colour.
- **The banner stays a rainbow** because the app labels that variant "pride".
- **No lettering** anywhere except the "P" on the parking sign.

## Checked

- The three new sheets are the same pixel size as the originals.
- No new sprite paints outside the footprint of the sprite it replaces, on any sheet.
- The Figma file holds the same sheets as editable vectors, one named group per sprite.

## Not done

- **Nothing is wired into the app.** `public/images` is untouched and the app has not been run with the new sheets. Swapping them in is a copy of three PNGs plus the two sky files.
- **People**: the live app takes its 31 figures from the external `streetmix-illustrations` package, which this session could not open. The new figures follow the widths in `segments/people.js` but their box size is an assumption.
- **UI icons, favicon, "learn more" photos, UI colours and fonts** are inventoried above but not redrawn or changed.
- **Colour values** were sampled from the brand book PDF. Check them against the Brand Toolkit before anything ships.
