# IMALOO world schema

Worlds are data, not code. Adding a world never needs an app rebuild: add one line to
`data/worlds.json`, one file in `data/worlds/`, and the photos in `worlds/<folder>/`.

## data/worlds.json (the library)

```json
{ "id": "deep-forest", "name": "Deep Forest", "thumb": "worlds/thumbs/deep-forest.jpg",
  "tone": ["#2f4a35", "#8fb07a"], "data": "data/worlds/deep-forest.json" }
```

`tone` is the gradient shown while the picture loads. Leave out `data` and the card shows
"Soon" until the world is ready.

## data/worlds/<id>.json (one world)

| Field | Meaning |
|---|---|
| `id`, `name`, `description` | Identity |
| `start` | Location the toy arrives in |
| `timeOfDay` | Allowed: `morning`, `day`, `sunset`, `night` |
| `weather` | Allowed: `sunny`, `cloudy`, `rain`, `fog` (`storm`, `snow` also handled by effects) |
| `locations[]` | The explorable places (below) |

All positions are fractions of the picture: `x` 0 (left) to 1 (right), `y` 0 (top) to 1 (bottom).
Pictures are 16:9; each has a full image (about 1920px) and a `-sm.jpg` (640px) for fast first paint.

### A location

| Field | Meaning |
|---|---|
| `id`, `name` | Identity |
| `image`, `imageSm` | Hero photo and small preview |
| `tone` | Placeholder colours |
| `surface` | `grass`, `sand`, `dirt`, `snow`, `floor`, `water`: sets footprints and sounds |
| `lighting` | `from` (sun direction in degrees, 0 = from the right, 90 = overhead), `warmth` (-1 cool to 1 warm), `shadow` (0–1 strength), `backlit` |
| `defaultTime` | Optional time this place opens at |
| `ground` | `horizon` (y of the horizon) and `nearScale` (toy height as a share of picture height at the bottom edge). The toy shrinks towards the horizon. |
| `walk` | Polygon `[[x,y],…]` of safe ground. Taps outside are moved to the nearest edge. |
| `spawn` | `[x,y]` where the toy stands on arrival |
| `foreground` | Occluders: `{ "polygon": [[x,y],…], "baseY": y }` (`baseY` defaults to the lowest point). Cut from the same photo and drawn in front of the toy when the toy stands behind `baseY` (rocks, trunks, fences). |
| `lights` | Optional `[[x,y],…]` fairy lights that glow at night or when switched on |
| `nav[]` | `{ "to": "<location id>", "x", "y" }` round picture doors to other places |
| `interactions[]` | `{ "id", "x", "y", "kind", "fx", "story" }`. `kind` picks the icon and toy animation (jump, hop, splash, sit, peek, climb, wonder, slide, knock, wave, dig, smell, build, lights). `fx` bursts `splash`, `sand` or `sparkle`. `story` uses `{name}` for the toy's name. |
| `discoveries[]` | `{ "id", "x", "y", "item", "near", "story" }` hidden until the toy walks within `near`. `item` is an icon from `js/icons.js`. |
| `ambient[]` | `{ "type", "area": [x,y,w,h], "n", "fall", "warm" }`. Types: dust, fireflies, stars, leaves, butterflies, bees, birds, water, mist, waves, sand, bubbles, rain, snow. Night swaps daytime creatures for fireflies and stars automatically. |
| `sound` | Soundscape: forest, creek, waterfall, waves, waves-far, waves-calm, backyard, indoors |

## Safety rules for new worlds

No weapons, horror, injury or danger. Storms and the dark should feel cosy and adventurous.
Every interaction ends happily.
