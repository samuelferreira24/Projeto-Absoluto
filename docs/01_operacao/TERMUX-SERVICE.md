# ABS + termux-services

This is the first service layer for keeping the local ABS process alive on Android.

## Architecture

Android boot
→ Termux:Boot
→ termux-services / runit
→ ABS service
→ abs_core.local

## Installation on the phone

From the repository root:

    bash scripts/termux/install_abs_service.sh

Then enable and start:

    sv-enable abs
    sv up abs

Check:

    sv status abs
    curl -s http://127.0.0.1:8787/health

## Boot

Copy or link scripts/termux/boot-start-services.sh into:

    ~/.termux/boot/start-services

and make it executable.

## Logs

Service logs are written to:

    ~/.abs/log

## Important

This service layer is compatible with the ABS update manager. The update manager can be installed separately with `scripts/termux/install_abs_update_manager.sh`; update application remains protected by explicit authorization, health validation and rollback.
