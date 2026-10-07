# ABS Browser

Base Android do Projeto Absoluto a partir do Mozilla Reference Browser.

## Upstream
- Repository: https://github.com/mozilla-mobile/reference-browser
- Upstream branch: master
- Purpose: browser capability/component, not the ABS core.

## Current strategy
1. CI fetches the upstream source.
2. The source is copied into this repository under this directory.
3. The build transforms the application identity to the ABS namespace.
4. Future ABS changes are applied on top of the pinned upstream revision.
5. Releases will use a stable ABS signing key and a separate update channel.

The generated APK is an artifact of the build; source remains authoritative.
