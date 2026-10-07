# IMALOO clickable prototype

`index.html` is a single-file web prototype of the IMALOO kids app (no build step).

Flow: Make a movie -> pick or photograph up to 3 toys -> name a new toy -> pick a world (Flower Garden, Fairy Forest, Bedroom to Space, Bedroom Castle) -> 30-second animated movie with read-aloud story and music -> Watch on TV (full screen) / Keep this movie (My movies library).

Prototype limits: movies are drawn live in the browser from story templates (no AI yet); photos and saved movies stay in the browser's local storage; "Watch on TV" goes full screen (real casting needs the native app).

## Run it

Open `index.html` in a browser, or serve the folder with any static web server (for example `npx serve .`). There is no build step.

## Hosting

Live at https://imaloo.ambiencecarewa.awesomate.app (Awesomate static app "imaloo").

Pushing to `main` does not update the live site. After a change, copy `index.html` up to the imaloo app again with the Awesomate tools (ask Claude to republish). The address is public; there is no private preview copy.

## How the app is built (2026-10 world system)

A static app with no build step: `index.html`, `css/app.css`, `js/*.js` (ES modules), `sw.js`.
Worlds are data: `data/worlds.json` lists all 27, and each playable world has its own file in
`data/worlds/`. Photos live in `worlds/<world>/` (plus `worlds/thumbs/`), toy pictures in `toys/`.
See [docs/world-schema.md](docs/world-schema.md) to add a world.

To publish, copy **every file and folder** to the Awesomate app (not just index.html).
To try it locally: `python3 -m http.server` in this folder, then open http://localhost:8000.
