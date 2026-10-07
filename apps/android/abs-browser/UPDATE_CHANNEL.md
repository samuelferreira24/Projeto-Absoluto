# ABS Android Update Channel

## Pipeline

The ABS Browser branch now has a manual release pipeline that fetches the Mozilla Reference Browser source, applies the ABS package identity, builds the APK, calculates SHA-256, publishes the APK as a GitHub Actions artifact, and generates `update/latest.json`.

## Remaining requirement

Real Android updates require the same signing key for every release. The private key must never be committed. It must be supplied as a GitHub Actions secret and used by the release workflow.

Normal Android installations require user confirmation. Silent installation requires special device privileges and is not assumed.

## Manifest contract

```json
{
  "appId": "org.projetoabsoluto.abs.browser",
  "versionName": "0.1.0",
  "versionCode": 1,
  "apkUrl": "...",
  "sha256": "...",
  "mandatory": false
}
```
