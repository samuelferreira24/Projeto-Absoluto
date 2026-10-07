# ABS Android Update Channel

The installed APK will use the Android package identity owned by Projeto Absoluto.

Target flow:

GitHub source -> CI build -> signed ABS APK -> update manifest/server -> installed ABS app

Required for real in-app updates:
- stable release signing key (never committed)
- monotonically increasing Android versionCode
- HTTPS update endpoint
- update manifest with version, versionCode, APK URL and SHA-256
- Android package installer confirmation for normal devices

The first bootstrap build deliberately does not pretend to have silent/system-level installation privileges.
