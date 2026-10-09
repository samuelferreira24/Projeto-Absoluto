# ABS Browser Control

## Purpose

The ABS browser is a persistent Chromium session hosted on `abs-vps-01`. The interactive web UI is bound to IPv4 loopback at `127.0.0.1:3000`; Chromium DevTools Protocol (CDP), when enabled, is bound only to `127.0.0.1:9222`. Neither endpoint is intended to be published directly to the Internet.

## Deployment layout

- Container: `abs-browser-ui` using `lscr.io/linuxserver/chromium`.
- Persistent profile: `/home/absadmin/abs-browser/config` mounted at `/config`.
- Protected credentials: `/home/absadmin/.config/abs-browser/browser.env`, permissions `0600`.
- Backups: `/home/absadmin/abs-browser/backups/profile-YYYY-MM-DD.tar.gz`, permissions `0600`.
- Resource limits: 1.5 CPU, 1280 MiB RAM, 1792 MiB RAM+swap, 512 MiB shared memory, 512 processes.
- ABS adapter: `abs_core/browser_adapter.py`, registered only when `ABS_BROWSER_CDP_URL=http://127.0.0.1:9222` is configured.

## ABS adapter actions

The capability ID is `browser-control`. Supported actions are:

- `status`: confirms that Chromium CDP responds and returns a browser version without exposing its WebSocket URL.
- `list_tabs`: returns tab IDs, titles, URLs and types.
- `open_url`: creates a tab for an HTTP(S) URL. It requires explicit approval in the capability context.

The adapter rejects non-HTTP(S) schemes, URLs containing embedded credentials, localhost/private literal IP destinations, common local hostnames and—when configured—hosts outside `ABS_BROWSER_ALLOWED_HOSTS`. With no explicit allowlist it resolves hostnames and rejects any result containing non-global IP addresses. This is a guardrail, not a substitute for network egress controls or human review of untrusted destinations.

## Live API smoke test

After deployment, the self-hosted workflow creates a work with context `{"action":"status"}` and runs it using capability `browser-control` with approval. A successful result must have state `completed` and result type `browser_status`.

For an approved navigation, the work context must include `{"action":"open_url","url":"https://example.com","approved":true}`; the run request itself must also be approved. Do not allow untrusted model output to grant approval automatically.

## Backup and recovery

The complete `config` directory is archived after gracefully stopping the browser. The workflow extracts the archive into a temporary staging directory and compares SHA-256 manifests file by file; it never overwrites the live profile during the restore test. Same-day backups rotate atomically through a temporary archive. A real restore into the live profile should only be performed during a planned recovery with the browser stopped and a separate copy of the current profile retained.

## Private mobile access

Use Tailscale Serve for private HTTPS access to `http://127.0.0.1:3000` only after Tailscale is installed and authenticated. Do not expose ports 3000 or 9222 through Docker public bindings, UFW, Coolify/Traefik, or a public reverse proxy. Tailscale authentication is an external identity step and cannot be completed on behalf of the account owner without their authorization.

## Verification evidence

The authoritative evidence is the run report posted by the GitHub Actions workflow `ABS Browser Complete All` on issue #121, plus its job logs. A workflow file existing in the repository is not evidence of a successful deployment. Record each item as PASS, BLOCKED, or NOT TESTED in the run report; do not infer mobile access from a local HTTP check.
