# ABS — Integration Architecture V1

## Objective

Web, Android/app, Termux, local servers, remote servers and future nodes do not need to be the same implementation. They need stable integration contracts.

## Rule

**Different surfaces, shared contracts.**

A surface is a client or runtime entry point. It is not the ABS itself.

```
Imperador
   │
   ├── Web
   ├── App
   ├── Termux
   ├── Server
   └── Remote Node
          │
          ▼
   ABS Integration Boundary
          │
   ├── API
   ├── identity/auth
   ├── state
   ├── Work
   ├── capabilities
   ├── resources
   └── events
          │
          ▼
       ABS Core
```

## V1 implementation

The repository has one composition root: `abs_core.runtime.build_runtime()`.

`abs_core.local` and `abs_core.server` remain separate launchers, but both construct the same runtime. This prevents one launcher from silently omitting cognitive, planning or dispatch layers.

## HTTP contract

The first concrete integration transport is HTTP/JSON. The contract is versioned under `/api/v1`.

The same endpoint is also available at the legacy path during the transition, so existing clients do not need to break immediately.

OpenAPI is published at:

`/api/v1/openapi.json`

The contract is intentionally client-oriented rather than UI-oriented. An Android app, browser, another server or another ABS node can implement its own experience and consume the same operations.

## State ownership

Clients may cache presentation state, but authoritative Work and cognitive-session state remains in ABS persistence.

Closing or minimizing a browser/app must not mean stopping a Work.

## Integration boundaries

```
surface
   ↓
versioned integration API
   ↓
ABS runtime
   ↓
capability / resource routing
   ↓
adapter
   ↓
external resource
```

A connection is not a capability. A capability is not an interface. This separation allows one service to be reached through multiple transports and allows multiple interfaces to use the same capability.

## Events

Work already contains structured events. V1 keeps Work state polling as the reliable baseline for clients. SSE/WebSocket delivery can be added later without changing the Work identity or state contract.

## Evolution

V1:
- shared runtime composition
- versioned HTTP boundary
- OpenAPI contract
- persistent Work/session state
- replaceable clients
- legacy compatibility during migration

Next:
- authenticated remote nodes
- SSE/WebSocket event delivery
- capability discovery between nodes
- delegated multi-AI orchestration
- remote device execution
- additional transports
