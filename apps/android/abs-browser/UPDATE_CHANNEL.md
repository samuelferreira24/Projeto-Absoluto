# ABS Android Update Channel

## Prototype pipeline

The ABS Browser prototype is built automatically from the Mozilla Reference Browser template. The release workflow:

1. fetches the upstream source;
2. applies the ABS application id `org.projetoabsoluto.abs.browser`;
3. injects the requested Android version name/code;
4. builds the prototype APK;
5. calculates SHA-256;
6. publishes the APK as a GitHub Actions artifact;
7. publishes the APK and checksum as a GitHub Release;
8. generates `update/latest.json` pointing to that release.

The prototype uses the normal Android debug/test signing path. A production signing key is intentionally not part of this stage.

## Update manifest

```json
{
  "appId": "org.projetoabsoluto.abs.browser",
  "versionName": "0.1.0",
  "versionCode": 1,
  "apkUrl": "https://github.com/samuelferreira24/Projeto-Absoluto/releases/download/abs-browser-v0.1.0/ABS-Browser-0.1.0.apk",
  "sha256": "...",
  "mandatory": false,
  "channel": "prototype"
}
```

## Important Android limitation

An ordinary Android application cannot silently replace itself. The prototype can download/prepare an update, but final installation still goes through Android's package-installer confirmation unless the device has special management/root privileges.

## Production later

Before calling this a production release channel, replace the prototype signing path with a permanent ABS release keystore stored as a GitHub Actions secret. Every future version must use that same signing identity.

The updater itself remains a separate implementation step: it needs to be integrated into the ABS app UI/runtime rather than being implied by the manifest alone.
