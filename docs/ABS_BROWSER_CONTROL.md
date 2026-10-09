# ABS Browser Control

## Purpose

The ABS browser is a persistent Chromium session hosted on `abs-vps-01`. The browser container uses host networking so Chromium's loopback-only DevTools Protocol endpoint is reachable by ABS at `127.0.0.1:9222`. The LinuxServer web UI listens on host ports 3000/3001; UFW has explicit inbound DENY rules for 3000, 3001 and 9222. These ports must not be opened in the provider firewall, Docker proxy, UFW allow rules, or a public reverse proxy. Private access is intended to use Tailscale Serve to `http://127.0.0.1:3000` after Tailscale account authentication.

## Deployment layout

- Container: `abs-browser-ui` using `lscr.io/linuxserver/chromium`.
- Persistent configuration volume: `/home/absadmin/abs-browser/config` mounted at `/config`.
- Active Chromium user-data directory: `/home/absadmin/abs-browser/config/chromium-abs-profile`; it is a non-default profile copied from the prior profile when available. The source profile remains in the volume.
- Protected credentials: `/home/absadmin/.config/abs-browser/browser.env`, permissions `0600`.
- Backups: `/home/absadmin/abs-browser/backups/profile-YYYY-MM-DD.tar.gz`, permissions `0600`.
- Resource limits: 1.5 CPU, 1280 MiB RAM, 1792 MiB RAM+swap, 512 MiB shared memory, 512 processes.
- Inbound firewall: explicit UFW DENY rules for TCP 3000, 3001 and 9222. No public Docker port mappings are used in host-network mode.
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

Use Tailscale Serve for private HTTPS access to `http://127.0.0.1:3000`. The systemd unit `abs-browser-tailnet-serve.service` waits for Tailscale to authenticate and then configures Serve automatically. The account owner must complete the initial Tailscale login; this external identity step cannot be performed on their behalf. Do not expose ports 3000, 3001 or 9222 through public Docker bindings, UFW allow rules, Coolify/Traefik, or a public reverse proxy.

## Verification evidence

The authoritative evidence is the run report posted by the GitHub Actions workflow `ABS Browser Complete All` on issue #121, plus its job logs. A workflow file existing in the repository is not evidence of a successful deployment. Record each item as PASS, BLOCKED, or NOT TESTED in the run report; do not infer mobile access from a local HTTP check.
