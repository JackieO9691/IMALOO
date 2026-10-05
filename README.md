# IMALOO clickable prototype

`index.html` is a single-file web prototype of the IMALOO kids app (no build step).

Flow: Make a movie -> pick or photograph up to 3 toys -> name a new toy -> pick a world (Flower Garden, Fairy Forest, Bedroom to Space, Bedroom Castle) -> 30-second animated movie with read-aloud story and music -> Watch on TV (full screen) / Keep this movie (My movies library).

Prototype limits: movies are drawn live in the browser from story templates (no AI yet); photos and saved movies stay in the browser's local storage; "Watch on TV" goes full screen (real casting needs the native app).

## Run it

Open `index.html` in a browser, or serve the folder with any static web server (for example `npx serve .`). There is no build step.

## Hosting

Deployed on Awesomate (hub.awesomate.ai) as a static app that rebuilds on every push to `main`.
