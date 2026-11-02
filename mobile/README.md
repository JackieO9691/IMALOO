# IMALOO phone apps (Google Play + Apple App Store)

Capacitor shell that opens the live web app (https://app.imaloo.com.au) inside a phone app, with app icon, splash screen, an offline "toys are napping" screen and camera/photo permissions.

- `capacitor.config.json` – app id `au.com.imaloo.app`, the address it opens
- `resources/` – icon and splash source pictures (`npx capacitor-assets generate` remakes all sizes)
- `android/`, `ios/` – native projects
- `STORE-LISTING.md` – store text draft
- Builds run on GitHub Actions (`.github/workflows/mobile-build.yml`): Android APK + AAB, iPhone simulator build. Signed store builds get added once the Apple and Google accounts exist (signing keys go in GitHub secrets, never in the repo).
