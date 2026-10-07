# IMALOO art direction (Jackie, 2026-10-07)

Jackie's three reference images set the look for everything: worlds, toys and the story replay.

- `art-direction/ref-worlds.png`: nine world scenes. **This is the world style.**
- `art-direction/ref-toys.png` and `art-direction/ref-teddy.png`: **this is the toy style.**

Use them as style references only. Don't copy any branded toy, such as a named fashion doll brand.

## Worlds

Make bright, warm, richly detailed storybook places that look like a glossy high-end 3D animated film still. Use these qualities:

- sunny, saturated colour;
- golden magical light with soft glow and light rays;
- soft depth of field;
- lots of charming small details, such as flowers, lanterns, bunting, mushrooms, butterflies and shells.

Avoid two things: gritty documentary photography and flat 2D cartoon.

Each world prompt starts with this style line:

> Bright, warm, magical children's storybook world rendered like a glossy high-end 3D animated film still, sunny saturated colours, golden glowing light and soft light rays, rich charming detail, soft depth of field, cosy and safe, wide 16:9 landscape, eye level of a small toy.

Then it adds these composition rules, so toys can be placed into the scene:

> Clear, open, flat, walkable ground across the lower third of the frame in the foreground, nothing standing on it. No people, no toys, no teddy bears, no characters and no animals in the foreground (small birds or butterflies in the distance are fine). No text, no signs with words, no watermark.

## Toys

The built-in toys are real, soft, photographed toys:

- plush fur you can almost feel, stitched details, shiny button eyes and ribbon bows;
- warm daylight;
- photographed on a plain light-grey studio background, then delivered as a transparent PNG with the background removed;
- the full body in frame, standing or sitting, facing three-quarter towards the camera.

Built-in set:

- `toys/teddy.png`: honey-brown shaggy teddy with a brown-cream plaid bow, matching `ref-teddy.png`.
- `toys/pony.png`: white plush unicorn pony with a fluffy pink mane, a sparkly pink saddle and a glittery horn.
- `toys/doll.png`: soft baby doll with a pink floral romper and a pink headband bow.

## Location prompts

These are the scene words added after the style line. The file paths stay the same.

### Deep Forest (`worlds/forest/`)

- `entrance`: a sunlit magical forest path between giant mossy trees, ferns, glowing mushrooms, wildflowers, hanging lanterns, and butterflies in the light rays.
- `creek`: a sparkling blue creek with round mossy stepping stones and a little wooden footbridge, flowers on the banks, with a mossy pebble bank in the foreground.
- `giant-tree`: a giant friendly tree with a round wooden door and glowing windows in its trunk, a little spiral stair, lanterns, a mushroom ring, and a soft grassy clearing in front.
- `waterfall`: a magical waterfall falling into a turquoise pool, rocks and ferns, with a sandy pool edge in the foreground.

### Australian Beach (`worlds/beach/`)

- `dunes`: a sandy path between soft grassy dunes, opening onto a bright turquoise sea and fluffy clouds.
- `main`: a sunny golden beach with gentle turquoise waves, a sandcastle with a little red flag, a bucket and spade, and shells.
- `rock-pools`: shallow sparkling rock pools with starfish, shells and a smiling little crab at the side, with flat wet sand in the foreground.
- `jetty`: a wooden jetty over calm water at golden sunset, a pink-orange sky, with soft sand in the foreground.

### Backyard Cubby House (`worlds/cubby/`)

- `backyard`: a wooden treehouse cubby in a big tree with fairy lights, bunting, a ladder, a green slide and a tyre swing, on a sunny green lawn with flowers.
- `inside`: a cosy cubby room with a round window, bunting, fairy lights, cushions, a little bookshelf, a lantern, a tea set on a small table and a rainbow rug, with an open wooden floor in the foreground.
- `garden`: a colourful backyard flower and vegetable garden with a sandpit holding a bucket and spade, and a garden path in the foreground.

### Preview thumbnails (`worlds/thumbs/<id>.jpg`)

Thumbnails use the same style line with the world's name and its most magical view. The 9 reference scenes map to these worlds:

- `deep-forest`: forest treehouse and waterfall
- `cubby`: backyard treehouse
- `aus-beach`: beach with sandcastle
- `park`: playground
- `bedroom`: cubby interior
- `rainforest`: rainforest waterfall
- `mountain`: rope bridge over a valley
- `farm`: red barn farm
- `space`: space deck with a rocket
