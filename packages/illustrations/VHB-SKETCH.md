# VHB marker-sketch artwork

This branch replaces part of the Streetmix illustration set with the VHB marker-sketch style: a loose ink line that
overshoots its corners, flat marker colour dropped in slightly off-register, and the VHB palette.

Every redrawn file keeps its original `viewBox` and draws into the footprint of the art it replaces, so sprite
positions defined in `packages/parts` are unchanged.

## Also changed outside this package

- `client/src/segments/view.ts`: the hard-coded ground colours (asphalt, concrete, bike and bus lane tints, sand, wall, earth).
- `client/src/sky/SkyBox/sky-front.svg`, `sky-rear.svg` and `public/images/sky-front.svg`, `sky-rear.svg`: sketch clouds.

## Redrawn (154 files)

- **bikes** (8): bike-rack-parallel-left, bike-rack-parallel-right, bike-rack-perpendicular-left, bike-rack-perpendicular-right, biker-01-inbound, biker-01-outbound, biker-02-inbound, biker-02-outbound
- **boundaries** (11): fenced-lot-left, fenced-lot-right, grass, parking-lot-left, parking-lot-right, water-left, water-right, waterfront-left, waterfront-right, waterfront2-left, waterfront2-right
- **buildings** (6): apartments-narrow-left, apartments-narrow-right, apartments-wide-left, apartments-wide-right, residential-left, residential-right
- **dividers** (3): bollard, dome, planter-box
- **furniture** (3): bench-center, bench-left, bench-right
- **ground** (8): asphalt-gray, asphalt-green, asphalt-red, asphalt, concrete, earth, sand, wall
- **lamps** (10): lamp-modern-both, lamp-modern-left, lamp-modern-right, lamp-traditional-both, lamp-traditional-center, lamp-traditional-left, lamp-traditional-right, lamp-traditional-with-base-wyc, pride-banner-left, pride-banner-right
- **parklet** (4): yerba-buena-parklet-left-v02, yerba-buena-parklet-left, yerba-buena-parklet-right-v02, yerba-buena-parklet-right
- **people** (46): people-01, people-02, people-03, people-04, people-05, people-06, people-07, people-08, people-09, people-10, people-11, people-12, people-13, people-14, people-15, people-16, people-17, people-18, people-19, people-20, people-21, people-22, people-23, people-24, people-25, people-26, people-27, people-28, people-29, people-30, people-31, people-32-back, people-32, people-33-back, people-33, people-34-back, people-34, people-35-back, people-35, people-36-back, people-36, people-37-back, people-37, people-38-back, people-38, people-39
- **plants** (7): bush, flowers-blue, flowers-orange, flowers-red, flowers-white, flowers-yellow, grass
- **secret** (1): inception-train
- **sky** (2): sky-front, sky-rear
- **transit** (14): bus-inbound-alt, bus-inbound, bus-outbound-alt, bus-outbound, light-rail-inbound, light-rail-outbound, streetcar-inbound, streetcar-outbound, tracks-dark, tracks-light, transit-shelter-01-left, transit-shelter-01-right, transit-shelter-02-left, transit-shelter-02-right
- **trees** (2): palm-tree, tree
- **vehicles** (26): car-angled-front-left, car-angled-front-right, car-angled-rear-left, car-angled-rear-right, car-inbound-door-left, car-inbound-door-right, car-inbound-turn-signal-left, car-inbound-turn-signal-right, car-inbound, car-outbound-door-left, car-outbound-door-right, car-outbound-turn-signal-left, car-outbound-turn-signal-right, car-outbound, car-sideways-left, car-sideways-right, rideshare-inbound-door-left, rideshare-inbound-door-right, rideshare-outbound-door-left, rideshare-outbound-door-right, taxi-inbound-door-left, taxi-inbound-door-right, taxi-outbound-door-left, taxi-outbound-door-right, truck-inbound, truck-outbound
- **wayfinding** (3): nyc-wayfinding-pylon-large, nyc-wayfinding-pylon-medium, nyc-wayfinding-pylon-small

## Still the original Streetmix art (182 files)

Road markings are left alone on purpose: they follow real-world standards and read the same in any style.
Everything else here simply has not been drawn yet, so streets that use these will show mixed styles.

- **beach** (2): lounger, surface
- **bikes** (2): bikeshare-left, bikeshare-right
- **boundaries** (12): beach-left, beach-right, cargo-ship-left, cargo-ship-right, compound-wall-left, compound-wall-right, dock-left, dock-right, fishing-boat-left, fishing-boat-right, marsh-left, marsh-right
- **buildings** (2): arcade-left, arcade-right
- **construction** (4): barricade, cone, jersey-barrier-concrete, jersey-barrier-plastic
- **curb** (4): person-waiting-01-left, person-waiting-01-right, pickup-sign-left, pickup-sign-right
- **dividers** (2): bike-lane-divider, guardrail
- **earth** (1): surface
- **effects** (4): electric, exclamation, sweat-drop, vein-pop
- **furniture** (2): cafe-seating-occupied, cafe-seating
- **markings** (35): both-inbound, both-outbound, center-lane-left, center-lane-right, center-lane, crosswalk-zebra-bike, crosswalk-zebra, lane-horiz, lane-left-half, lane-left, lane-right-half, lane-right, left-inbound, left-outbound, left-right-straight-inbound, left-right-straight-outbound, left-straight-inbound, left-straight-outbound, parking-left, parking-right, right-inbound, right-outbound, right-straight-inbound, right-straight-outbound, shared-inbound, shared-outbound, sharrow-inbound, sharrow-outbound, straight-inbound-light, straight-inbound, straight-outbound-light, straight-outbound, streetcar-track-01, streetcar-track-02, stripes-diagonal
- **(root)** (1): missing
- **people** (6): bernie, johnny-01, johnny-02, junebug-01, junebug-02, junebug-03
- **plants** (8): bioswale-pieces-slope-left, bioswale-pieces-slope-right, marsh-grass-01, marsh-grass-02, marsh-grass-03, marsh-grass-04, marsh-grass-05, marsh-grass-06
- **scooters** (6): scooter-inbound, scooter-left-docked, scooter-left-rider, scooter-outbound, scooter-right-docked, scooter-right-rider
- **sky** (6): holodeck-grid, icon-holodeck, icon-night, moon, stars, super-blood-wolf-moon
- **thumbnails** (38): beach, bike-lane, bikeshare, bioswale, brt-lane, brt-station, bus-lane, divider, drainage-channel, drive-lane, flex-zone-curb, flex-zone, food-truck, guardrail, light-rail, magic-carpet, marsh, missing, outdoor-dining, parking-lane, parklet, scooter-drop-zone, scooter, sidewalk-bench, sidewalk-bike-rack, sidewalk-lamp, sidewalk-tree, sidewalk-wayfinding, sidewalk, slope, street-vendor, streetcar, temporary, train, transit-shelter, turn-lane, utilities, wall
- **transit** (14): av-shuttle-inbound, av-shuttle-outbound, brt-bus-inbound, brt-bus-outbound, brt-station-center, brt-station-left, brt-station-piece-center, brt-station-piece-left-edge, brt-station-piece-left-platform, brt-station-piece-right-edge, brt-station-piece-right-platform, brt-station-right, double-decker-bus-inbound, double-decker-bus-outbound
- **utilities** (7): drainage-channel-piece-center, drainage-channel-piece-left-slanted, drainage-channel-piece-left-vertical, drainage-channel-piece-right-slanted, drainage-channel-piece-right-vertical, utility-pole-left, utility-pole-right
- **vehicles** (12): av-inbound, av-outbound, foodtruck-left, foodtruck-right, krz-motorbike-inbound, krz-motorbike-outbound, magic-carpet-aladdin-jasmine, magic-carpet-aladdin, magic-carpet-jasmine-aladdin, magic-carpet-jasmine, microvan-inbound, microvan-outbound
- **vendors** (4): vendor-handcart, vendor-platform, vendor-table, vendor-tarp
- **wall** (10): wall-high-center, wall-high-left-sloped, wall-high-left-straight, wall-high-right-sloped, wall-high-right-straight, wall-low-center, wall-low-left-sloped, wall-low-left-straight, wall-low-right-sloped, wall-low-right-straight

## Regenerating

The drawings are generated, not hand-edited. The generator lives in `vhb-restyle/tools/` on the
`claude/loving-ride-fkvnk3` branch of this fork (`upstream_measure.js`, then `upstream_export.py`).
